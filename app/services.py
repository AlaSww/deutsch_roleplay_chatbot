from __future__ import annotations

import json
from typing import Any

import groq
from flask import current_app
from groq import Groq

from .prompts import (
    build_conversation_system_prompt,
    build_final_feedback_system_prompt,
    build_final_feedback_user_prompt,
    build_opening_user_prompt,
    build_profile_update_system_prompt,
    build_profile_update_user_prompt,
    build_reply_summary_block,
    build_single_feedback_system_prompt,
    build_single_feedback_user_prompt,
)


def _get_client() -> Groq:
    api_key = current_app.config["GROQ_API_KEY"]
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing.")

    return Groq(
        api_key=api_key,
        timeout=current_app.config["GROQ_TIMEOUT"],
    )


def _extract_text(response: Any) -> str:
    content = response.choices[0].message.content or ""
    return content.strip()


def _chat(messages: list[dict[str, str]], *, model: str, temperature: float, max_completion_tokens: int) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
    )
    return _extract_text(response)


def _structured_chat(
    *,
    schema_name: str,
    schema: dict[str, Any],
    messages: list[dict[str, str]],
) -> dict[str, Any]:
    client = _get_client()
    response = client.chat.completions.create(
        model=current_app.config["GROQ_STRUCTURED_MODEL"],
        messages=messages,
        temperature=0.2,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        },
    )
    content = _extract_text(response)
    return json.loads(content)


def build_chat_history_messages(conversation: dict, history: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": build_conversation_system_prompt(conversation)}
    ]

    summary_block = build_reply_summary_block(conversation.get("conversation_summary"))
    if summary_block and len(history) > current_app.config["MAX_CONTEXT_MESSAGES"]:
        messages.append({"role": "system", "content": summary_block})

    trimmed_history = history[-current_app.config["MAX_CONTEXT_MESSAGES"] :]
    for item in trimmed_history:
        role = "assistant" if item["sender"] == "assistant" else "user"
        messages.append({"role": role, "content": item["content"]})

    return messages


def generate_opening_message(conversation: dict) -> str:
    messages = [
        {"role": "system", "content": build_conversation_system_prompt(conversation)},
        {"role": "user", "content": build_opening_user_prompt()},
    ]
    return _chat(
        messages,
        model=current_app.config["GROQ_CHAT_MODEL"],
        temperature=0.7,
        max_completion_tokens=280,
    )


def generate_assistant_reply(conversation: dict, history: list[dict[str, Any]]) -> str:
    messages = build_chat_history_messages(conversation, history)
    return _chat(
        messages,
        model=current_app.config["GROQ_CHAT_MODEL"],
        temperature=0.7,
        max_completion_tokens=320,
    )


def generate_single_message_feedback(
    conversation: dict,
    message: dict[str, Any],
    surrounding_messages: list[dict[str, Any]],
) -> dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {
            "feedback_summary": {"type": "string"},
            "corrected_text": {"type": "string"},
            "mistakes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "span": {"type": "string"},
                        "issue": {"type": "string"},
                        "category": {"type": "string"},
                    },
                    "required": ["span", "issue", "category"],
                    "additionalProperties": False,
                },
            },
            "better_alternatives": {
                "type": "array",
                "items": {"type": "string"},
            },
            "explanations": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "feedback_summary",
            "corrected_text",
            "mistakes",
            "better_alternatives",
            "explanations",
        ],
        "additionalProperties": False,
    }

    return _structured_chat(
        schema_name="single_message_feedback",
        schema=schema,
        messages=[
            {"role": "system", "content": build_single_feedback_system_prompt(conversation)},
            {
                "role": "user",
                "content": build_single_feedback_user_prompt(message, surrounding_messages),
            },
        ],
    )


def generate_final_feedback(conversation: dict, user_messages: list[dict[str, Any]]) -> dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {
            "overall_feedback": {"type": "string"},
            "message_feedback": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "message_id": {"type": "string"},
                        "feedback_summary": {"type": "string"},
                        "corrected_text": {"type": "string"},
                        "mistakes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "span": {"type": "string"},
                                    "issue": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                                "required": ["span", "issue", "category"],
                                "additionalProperties": False,
                            },
                        },
                        "better_alternatives": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "explanations": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "message_id",
                        "feedback_summary",
                        "corrected_text",
                        "mistakes",
                        "better_alternatives",
                        "explanations",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["overall_feedback", "message_feedback"],
        "additionalProperties": False,
    }

    return _structured_chat(
        schema_name="conversation_feedback",
        schema=schema,
        messages=[
            {"role": "system", "content": build_final_feedback_system_prompt(conversation)},
            {
                "role": "user",
                "content": build_final_feedback_user_prompt(user_messages),
            },
        ],
    )


def generate_updated_user_profile(
    conversation: dict,
    user_messages: list[dict[str, Any]],
    final_feedback: dict[str, Any],
    stored_feedback_items: list[dict[str, Any]],
) -> dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {
            "common_mistakes": {
                "type": "array",
                "items": {"type": "string"},
            },
            "grammar_focus_areas": {
                "type": "array",
                "items": {"type": "string"},
            },
            "vocabulary_gaps": {
                "type": "array",
                "items": {"type": "string"},
            },
            "strengths": {
                "type": "array",
                "items": {"type": "string"},
            },
            "last_feedback_summary": {"type": "string"},
        },
        "required": [
            "common_mistakes",
            "grammar_focus_areas",
            "vocabulary_gaps",
            "strengths",
            "last_feedback_summary",
        ],
        "additionalProperties": False,
    }

    return _structured_chat(
        schema_name="user_profile_update",
        schema=schema,
        messages=[
            {"role": "system", "content": build_profile_update_system_prompt(conversation)},
            {
                "role": "user",
                "content": build_profile_update_user_prompt(
                    conversation,
                    user_messages,
                    final_feedback,
                    stored_feedback_items,
                ),
            },
        ],
    )


def groq_error_message(error: Exception) -> str:
    if isinstance(error, groq.APIStatusError):
        return f"Groq API returned HTTP {error.status_code}."
    if isinstance(error, groq.APIConnectionError):
        return "Could not connect to Groq API."
    return str(error)
