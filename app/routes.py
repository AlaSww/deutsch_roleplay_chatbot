from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import psycopg
from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import auth_required, create_access_token
from . import repositories
from .prompts import build_summary_text
from .services import (
    generate_assistant_reply,
    generate_final_feedback,
    generate_opening_message,
    generate_single_message_feedback,
    generate_updated_user_profile,
    groq_error_message,
)


api = Blueprint("api", __name__)


def _json_ready(value):
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, UUID):
        return str(value)
    return value


def _error(message: str, status_code: int):
    return jsonify({"error": message}), status_code


def _is_valid_uuid(value: str | None) -> bool:
    if not value:
        return False
    try:
        UUID(str(value))
        return True
    except ValueError:
        return False


def _parse_body() -> dict:
    return request.get_json(silent=True) or {}


def _optional_list(payload: dict, field: str):
    value = payload.get(field)
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a JSON array.")
    return value


def _require_fields(payload: dict, fields: list[str]) -> str | None:
    for field in fields:
        value = payload.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            return field
    return None


def _conversation_or_404(conversation_id: str):
    conversation = repositories.get_conversation(conversation_id)
    if not conversation:
        return None, _error("Conversation not found.", 404)
    if str(conversation["user_id"]) != g.current_user_id:
        return None, _error("You are not allowed to access this conversation.", 403)
    return conversation, None


def _message_or_404(conversation_id: str, message_id: str):
    message = repositories.get_message(conversation_id, message_id)
    if not message:
        return None, _error("Message not found.", 404)
    return message, None


def _message_context(messages: list[dict], message_id: str, radius: int = 2) -> list[dict]:
    indices = {str(item["id"]): index for index, item in enumerate(messages)}
    if message_id not in indices:
        return []

    index = indices[message_id]
    start = max(0, index - radius)
    end = min(len(messages), index + radius + 1)
    return messages[start:end]


def _fallback_final_feedback(conversation: dict, all_messages: list[dict], user_messages: list[dict]) -> dict:
    message_feedback = []

    for message in user_messages:
        surrounding_messages = _message_context(all_messages, str(message["id"]))
        single_feedback = generate_single_message_feedback(
            conversation,
            message,
            surrounding_messages,
        )
        message_feedback.append(
            {
                "message_id": str(message["id"]),
                "feedback_summary": single_feedback["feedback_summary"],
                "corrected_text": single_feedback["corrected_text"],
                "mistakes": single_feedback["mistakes"],
                "better_alternatives": single_feedback["better_alternatives"],
                "explanations": single_feedback["explanations"],
            }
        )

    summary_lines = [item["feedback_summary"] for item in message_feedback if item["feedback_summary"]]
    overall_feedback = (
        "Conversation feedback was assembled from individual message reviews. "
        + " ".join(summary_lines[:4])
    ).strip()

    return {
        "overall_feedback": overall_feedback or "Feedback generated from individual message reviews.",
        "message_feedback": message_feedback,
    }


def _conversation_payload(conversation_id: str):
    conversation = repositories.get_conversation(conversation_id)
    if not conversation:
        return None
    if str(conversation["user_id"]) != g.current_user_id:
        return None

    messages = repositories.list_messages(conversation_id)
    feedback = repositories.list_feedback_for_conversation(conversation_id)
    conversation["messages"] = messages
    conversation["feedback"] = feedback
    return conversation


@api.get("/health")
def health():
    return jsonify({"status": "ok"})


@api.post("/auth/register")
def auth_register():
    payload = _parse_body()
    missing = _require_fields(payload, ["email", "password"])
    if missing:
        return _error(f"Missing required field: {missing}", 400)

    email = payload["email"].strip().lower()
    password = payload["password"]
    german_level = payload.get("german_level")
    native_language = payload.get("native_language")
    plan = (payload.get("plan") or "free").strip().lower()

    if plan not in {"free", "premium"}:
        return _error("plan must be either 'free' or 'premium'.", 400)
    if len(password) < 8:
        return _error("password must be at least 8 characters long.", 400)

    try:
        user = repositories.create_user(
            email,
            generate_password_hash(password),
            german_level,
            native_language,
            plan,
            common_mistakes=_optional_list(payload, "common_mistakes"),
            grammar_focus_areas=_optional_list(payload, "grammar_focus_areas"),
            vocabulary_gaps=_optional_list(payload, "vocabulary_gaps"),
            strengths=_optional_list(payload, "strengths"),
            last_feedback_summary=payload.get("last_feedback_summary"),
        )
    except ValueError as error:
        return _error(str(error), 400)
    except psycopg.errors.UniqueViolation:
        return _error("A user with this email already exists.", 409)

    token = create_access_token(user)
    return jsonify(_json_ready({"access_token": token, "user": user})), 201


@api.post("/auth/login")
def auth_login():
    payload = _parse_body()
    missing = _require_fields(payload, ["email", "password"])
    if missing:
        return _error(f"Missing required field: {missing}", 400)

    email = payload["email"].strip().lower()
    password = payload["password"]
    user = repositories.get_user_with_password_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return _error("Invalid email or password.", 401)

    public_user = repositories.get_user(str(user["id"]))
    token = create_access_token(public_user)
    return jsonify(_json_ready({"access_token": token, "user": public_user}))


@api.get("/auth/me")
@auth_required
def auth_me():
    return jsonify(_json_ready(g.current_user))


@api.get("/users")
@auth_required
def users_index():
    return jsonify(_json_ready([g.current_user]))


@api.get("/scenarios")
def scenarios_index():
    return jsonify(_json_ready(repositories.list_scenarios()))


@api.get("/scenarios/<scenario_id>")
def scenarios_show(scenario_id: str):
    if not _is_valid_uuid(scenario_id):
        return _error("scenario_id must be a valid UUID.", 400)

    scenario = repositories.get_scenario(scenario_id)
    if not scenario:
        return _error("Scenario not found.", 404)
    return jsonify(_json_ready(scenario))


@api.get("/conversations")
@auth_required
def conversations_index():
    conversations = repositories.list_conversations(g.current_user_id)
    return jsonify(_json_ready(conversations))


@api.post("/conversations")
@auth_required
def conversations_create():
    payload = _parse_body()
    missing = _require_fields(payload, ["scenario_id", "scenario_role_id"])
    if missing:
        return _error(f"Missing required field: {missing}", 400)

    for field in ["scenario_id", "scenario_role_id"]:
        if not _is_valid_uuid(payload[field]):
            return _error(f"{field} must be a valid UUID.", 400)

    scenario = repositories.get_scenario(payload["scenario_id"])
    if not scenario:
        return _error("Scenario not found.", 404)
    if len(scenario["roles"]) != 2:
        return _error("A scenario must have exactly two roles.", 400)

    role = repositories.get_scenario_role(payload["scenario_id"], payload["scenario_role_id"])
    if not role:
        return _error("Role not found for this scenario.", 404)

    conversation = repositories.create_conversation(
        g.current_user_id,
        payload["scenario_id"],
        payload["scenario_role_id"],
    )

    should_generate_opening = payload.get("generate_opening_message")
    if should_generate_opening is None:
        should_generate_opening = current_app.config["DEFAULT_OPENING_MESSAGE"]

    opening_message = None
    opening_message_error = None
    if should_generate_opening:
        enriched = repositories.get_conversation(str(conversation["id"]))
        try:
            opening_text = generate_opening_message(enriched)
            opening_message = repositories.create_message(
                str(conversation["id"]),
                "assistant",
                opening_text,
            )
            repositories.upsert_conversation_summary(
                str(conversation["id"]),
                build_summary_text([opening_message]),
            )
        except Exception as error:
            opening_message_error = groq_error_message(error)

    response_payload = repositories.get_conversation(str(conversation["id"]))
    if not response_payload.get("ai_role"):
        return _error("The selected scenario does not have a matching AI role.", 400)
    response_payload["messages"] = [opening_message] if opening_message else []
    response_payload["feedback"] = None
    if opening_message_error:
        response_payload["opening_message_error"] = opening_message_error
    return jsonify(_json_ready(response_payload)), 201


@api.get("/conversations/<conversation_id>")
@auth_required
def conversations_show(conversation_id: str):
    if not _is_valid_uuid(conversation_id):
        return _error("conversation_id must be a valid UUID.", 400)

    payload = _conversation_payload(conversation_id)
    if not payload:
        return _error("Conversation not found.", 404)
    return jsonify(_json_ready(payload))


@api.post("/conversations/<conversation_id>/messages")
@auth_required
def conversation_messages_create(conversation_id: str):
    if not _is_valid_uuid(conversation_id):
        return _error("conversation_id must be a valid UUID.", 400)

    conversation, error_response = _conversation_or_404(conversation_id)
    if error_response:
        return error_response

    if conversation["status"] != "active":
        return _error("Conversation is not active.", 400)
    if not conversation.get("ai_role"):
        return _error("This conversation does not have a matching AI role.", 400)

    payload = _parse_body()
    missing = _require_fields(payload, ["content"])
    if missing:
        return _error(f"Missing required field: {missing}", 400)

    user_message = repositories.create_message(
        conversation_id,
        "user",
        payload["content"].strip(),
    )

    history = repositories.list_messages(conversation_id)
    refreshed_conversation = repositories.get_conversation(conversation_id)

    try:
        assistant_text = generate_assistant_reply(refreshed_conversation, history)
        assistant_message = repositories.create_message(
            conversation_id,
            "assistant",
            assistant_text,
        )
    except Exception as error:
        return (
            jsonify(
                _json_ready(
                    {
                        "error": groq_error_message(error),
                        "user_message": user_message,
                    }
                )
            ),
            502,
        )

    updated_messages = repositories.list_messages(conversation_id)
    repositories.upsert_conversation_summary(
        conversation_id,
        build_summary_text(updated_messages),
    )

    return jsonify(
        _json_ready(
            {
                "user_message": user_message,
                "assistant_message": assistant_message,
            }
        )
    ), 201


@api.post("/conversations/<conversation_id>/messages/<message_id>/feedback")
@auth_required
def conversation_message_feedback(conversation_id: str, message_id: str):
    if not _is_valid_uuid(conversation_id):
        return _error("conversation_id must be a valid UUID.", 400)
    if not _is_valid_uuid(message_id):
        return _error("message_id must be a valid UUID.", 400)

    conversation, error_response = _conversation_or_404(conversation_id)
    if error_response:
        return error_response

    message, error_response = _message_or_404(conversation_id, message_id)
    if error_response:
        return error_response

    if message["sender"] != "user":
        return _error("Feedback can only be generated for user messages.", 400)

    all_messages = repositories.list_messages(conversation_id)
    surrounding_messages = _message_context(all_messages, message_id)

    try:
        feedback_payload = generate_single_message_feedback(
            conversation,
            message,
            surrounding_messages,
        )
    except Exception as error:
        return _error(groq_error_message(error), 502)

    feedback_session = repositories.get_or_create_feedback_session(conversation_id)
    saved_feedback = repositories.upsert_message_feedback(
        str(feedback_session["id"]),
        message_id,
        message["content"],
        feedback_payload["corrected_text"],
        feedback_payload["mistakes"],
        feedback_payload["better_alternatives"],
        feedback_payload["explanations"],
    )

    return jsonify(
        _json_ready(
            {
                "feedback_session_id": feedback_session["id"],
                "feedback_summary": feedback_payload["feedback_summary"],
                "message_feedback": saved_feedback,
            }
        )
    )


@api.get("/conversations/<conversation_id>/feedback")
@auth_required
def conversation_feedback_show(conversation_id: str):
    if not _is_valid_uuid(conversation_id):
        return _error("conversation_id must be a valid UUID.", 400)

    conversation, error_response = _conversation_or_404(conversation_id)
    if error_response:
        return error_response
    if not conversation.get("ai_role"):
        return _error("This conversation does not have a matching AI role.", 400)

    feedback = repositories.list_feedback_for_conversation(str(conversation["id"]))
    if not feedback:
        return _error("No feedback has been generated for this conversation yet.", 404)

    return jsonify(_json_ready(feedback))


@api.post("/conversations/<conversation_id>/complete")
@auth_required
def conversations_complete(conversation_id: str):
    if not _is_valid_uuid(conversation_id):
        return _error("conversation_id must be a valid UUID.", 400)

    conversation, error_response = _conversation_or_404(conversation_id)
    if error_response:
        return error_response
    if not conversation.get("ai_role"):
        return _error("This conversation does not have a matching AI role.", 400)

    messages = repositories.list_messages(conversation_id)
    user_messages = [item for item in messages if item["sender"] == "user"]
    if not user_messages:
        return _error("Conversation has no user messages to evaluate.", 400)

    final_feedback_error = None
    try:
        feedback_payload = generate_final_feedback(conversation, user_messages)
    except Exception as error:
        final_feedback_error = groq_error_message(error)
        try:
            feedback_payload = _fallback_final_feedback(conversation, messages, user_messages)
        except Exception:
            return _error(final_feedback_error, 502)

    feedback_session = repositories.get_or_create_feedback_session(conversation_id)
    stored_feedback_items = []
    feedback_by_message_id = {
        item["message_id"]: item for item in feedback_payload["message_feedback"]
    }

    for message in user_messages:
        feedback_item = feedback_by_message_id.get(str(message["id"]))
        if not feedback_item:
            feedback_item = {
                "corrected_text": message["content"],
                "mistakes": [],
                "better_alternatives": [],
                "explanations": ["No detailed feedback was generated for this message."],
            }

        stored_feedback_items.append(
            repositories.upsert_message_feedback(
                str(feedback_session["id"]),
                str(message["id"]),
                message["content"],
                feedback_item["corrected_text"],
                feedback_item["mistakes"],
                feedback_item["better_alternatives"],
                feedback_item["explanations"],
            )
        )

    updated_session = repositories.update_feedback_session(
        str(feedback_session["id"]),
        feedback_payload["overall_feedback"],
    )
    repositories.complete_conversation(conversation_id)
    repositories.upsert_conversation_summary(
        conversation_id,
        build_summary_text(messages),
    )

    profile_update = None
    profile_update_error = None
    refreshed_conversation = repositories.get_conversation(conversation_id)
    try:
        profile_payload = generate_updated_user_profile(
            refreshed_conversation,
            user_messages,
            feedback_payload,
            stored_feedback_items,
        )
        profile_update = repositories.update_user_profile(
            str(conversation["user_id"]),
            common_mistakes=profile_payload["common_mistakes"],
            grammar_focus_areas=profile_payload["grammar_focus_areas"],
            vocabulary_gaps=profile_payload["vocabulary_gaps"],
            strengths=profile_payload["strengths"],
            last_feedback_summary=profile_payload["last_feedback_summary"],
        )
    except Exception as error:
        profile_update_error = groq_error_message(error)

    return jsonify(
        _json_ready(
            {
                "feedback_session": updated_session,
                "message_feedback": stored_feedback_items,
                "user_profile": profile_update,
                "profile_update_error": profile_update_error,
                "final_feedback_error": final_feedback_error,
            }
        )
    )
