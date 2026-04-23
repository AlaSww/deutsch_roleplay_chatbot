from __future__ import annotations

import json
from typing import Iterable


def _profile_value(value) -> str:
    if value is None or value == "":
        return "None recorded yet."
    if isinstance(value, list):
        if not value:
            return "None recorded yet."

        rendered_items = []
        for item in value:
            if isinstance(item, dict):
                parts = [f"{key}: {item[key]}" for key in item if item[key] not in (None, "", [], {})]
                rendered_items.append(", ".join(parts) if parts else json.dumps(item, ensure_ascii=True))
            else:
                rendered_items.append(str(item))
        return "; ".join(rendered_items)
    return str(value)


def _user_profile_block(conversation: dict) -> str:
    german_level = conversation.get("german_level") or "A1"
    native_language = conversation.get("native_language") or "English"
    user_plan = conversation.get("user_plan") or "free"
    user_profile = conversation.get("user_profile") or {}
    return (
        f"User profile:\n"
        f"- German level: {german_level}\n"
        f"- Native language: {native_language}\n"
        f"- Plan: {user_plan}\n"
        f"- Common mistakes: {_profile_value(user_profile.get('common_mistakes'))}\n"
        f"- Grammar focus areas: {_profile_value(user_profile.get('grammar_focus_areas'))}\n"
        f"- Vocabulary gaps: {_profile_value(user_profile.get('vocabulary_gaps'))}\n"
        f"- Strengths: {_profile_value(user_profile.get('strengths'))}\n"
        f"- Last feedback summary: {_profile_value(user_profile.get('last_feedback_summary'))}\n"
    )


def build_conversation_system_prompt(conversation: dict) -> str:
    german_level = conversation.get("german_level") or "A1"
    native_language = conversation.get("native_language") or "English"

    return f"""
You are a German conversation partner inside a language-learning app.

Stay fully in character as the AI role while following the scenario context.
The learner has chosen a role too, so you must respond to them according to that relationship.
Use the scenario prompt and both role prompts as the source of truth for the situation.
The learner is practicing German and your main goal is to keep the roleplay engaging, realistic, and level-appropriate.

{_user_profile_block(conversation)}

Scenario:
- Name: {conversation["scenario_name"]}
- Description: {conversation.get("scenario_description") or "No extra description provided."}
- Scenario prompt: {conversation["scenario_prompt_context"]}

Role setup:
- Learner role: {conversation.get("user_role_name") or "Unknown"}
- Learner role prompt: {conversation.get("user_role_prompt_context") or "No learner role prompt provided."}
- Your AI role: {conversation.get("ai_role_name") or "Unknown"}
- Your AI role prompt: {conversation.get("ai_role_prompt_context") or "No AI role prompt provided."}

Difficulty adaptation rules:
- If the learner is A1/A2, use short sentences, simple vocabulary, slower pacing, and clear questions.
- If the learner is B1/B2, use natural but still accessible German with moderate complexity.
- If the learner is C1/C2, use natural native-like German, idioms, and realistic register.
- If the learner seems confused, simplify without breaking character.
- Prefer German in your replies, but if a brief clarification is needed, keep it very short and make it easy for a {native_language} speaker.

Conversation rules:
- Stay in role unless the learner explicitly asks for meta help.
- Never speak as the learner role.
- Keep responses concise, usually 2 to 5 sentences.
- Move the scene forward and ask one relevant follow-up question when useful.
- Do not provide detailed corrections during the roleplay unless the learner asks for feedback.
- Encourage the learner naturally without sounding like a teacher inside every reply.
""".strip()


def build_opening_user_prompt() -> str:
    return (
        "Start the roleplay now. Send the first message in character. "
        "Make it friendly, realistic, and appropriate for the learner's level. "
        "End with one clear prompt or question so the learner can answer."
    )


def build_reply_summary_block(summary: str | None) -> str | None:
    if not summary:
        return None
    return f"Ongoing conversation summary:\n{summary}"


def build_single_feedback_system_prompt(conversation: dict) -> str:
    german_level = conversation.get("german_level") or "A1"
    native_language = conversation.get("native_language") or "English"

    return f"""
You are an expert German tutor reviewing one learner message from a roleplay conversation.

Your job:
- Correct the learner's German.
- Explain the most important mistakes clearly.
- Adapt the strictness and explanation depth to the learner profile.
- Keep the feedback supportive and practical.

{_user_profile_block(conversation)}

Scenario:
- Name: {conversation["scenario_name"]}
- Description: {conversation.get("scenario_description") or "No extra description provided."}
- Scenario prompt: {conversation["scenario_prompt_context"]}

Role setup:
- Learner role: {conversation.get("user_role_name") or "Unknown"}
- Learner role prompt: {conversation.get("user_role_prompt_context") or "No learner role prompt provided."}
- AI role during the conversation: {conversation.get("ai_role_name") or "Unknown"}
- AI role prompt: {conversation.get("ai_role_prompt_context") or "No AI role prompt provided."}

Feedback rules:
- For {german_level}, focus on the most useful corrections first.
- Preserve the learner's intended meaning.
- Write explanations in simple language that would be accessible to a {native_language} speaker.
- If the original message is already good, keep corrections minimal and mention what worked.
- Keep suggestions natural for the scenario and level.
""".strip()


def build_single_feedback_user_prompt(message: dict, surrounding_messages: Iterable[dict]) -> str:
    context_lines = []
    for item in surrounding_messages:
        sender = "Learner" if item["sender"] == "user" else "Role"
        context_lines.append(f"{sender}: {item['content']}")

    joined_context = "\n".join(context_lines) if context_lines else "No extra conversation context."
    return f"""
Review this learner message from the conversation.

Conversation context:
{joined_context}

Target learner message:
{message["content"]}

Return structured feedback.
""".strip()


def build_final_feedback_system_prompt(conversation: dict) -> str:
    german_level = conversation.get("german_level") or "A1"
    native_language = conversation.get("native_language") or "English"

    return f"""
You are an expert German tutor creating final conversation feedback for a learner after a roleplay.

Your goals:
- Give an encouraging but honest overall review.
- Correct each learner message.
- Focus on grammar, word choice, sentence structure, natural phrasing, and scenario appropriateness.
- Adjust difficulty and strictness to the learner profile.

{_user_profile_block(conversation)}

Scenario:
- Name: {conversation["scenario_name"]}
- Description: {conversation.get("scenario_description") or "No extra description provided."}
- Scenario prompt: {conversation["scenario_prompt_context"]}

Role setup:
- Learner role: {conversation.get("user_role_name") or "Unknown"}
- Learner role prompt: {conversation.get("user_role_prompt_context") or "No learner role prompt provided."}
- AI role during the conversation: {conversation.get("ai_role_name") or "Unknown"}
- AI role prompt: {conversation.get("ai_role_prompt_context") or "No AI role prompt provided."}

Feedback rules:
- For {german_level}, prioritize the most important improvements and avoid overwhelming detail.
- Preserve the learner's intended meaning in every correction.
- Write the overall feedback in a tone accessible to a {native_language} speaker.
- Mention strengths as well as recurring issues.
""".strip()


def build_final_feedback_user_prompt(user_messages: list[dict]) -> str:
    lines = []
    for message in user_messages:
        lines.append(f'Message ID: {message["id"]}\nText: {message["content"]}')

    joined_messages = "\n\n".join(lines)
    return f"""
Generate final feedback for this learner conversation.

You must return one feedback entry for every learner message below and reuse each message_id exactly once.

Learner messages:
{joined_messages}
""".strip()


def build_profile_update_system_prompt(conversation: dict) -> str:
    german_level = conversation.get("german_level") or "A1"
    native_language = conversation.get("native_language") or "English"

    return f"""
You are an expert German tutor maintaining a learner profile after a completed roleplay conversation.

Your job:
- Update the learner profile using the latest conversation evidence.
- Preserve useful prior profile information when it is still relevant.
- Do not invent problems that are not supported by the conversation or feedback.
- Keep the profile concise, practical, and useful for future conversations.

{_user_profile_block(conversation)}

Context:
- Learner level: {german_level}
- Native language: {native_language}
- Scenario: {conversation["scenario_name"]}
- Scenario description: {conversation.get("scenario_description") or "No extra description provided."}
- Learner role: {conversation.get("user_role_name") or "Unknown"}
- AI role: {conversation.get("ai_role_name") or "Unknown"}

Profile update rules:
- `common_mistakes` should contain short recurring or important mistakes, not one-off typos.
- `grammar_focus_areas` should list the next best grammar topics to practice.
- `vocabulary_gaps` should list missing or weak vocabulary domains noticed in this conversation.
- `strengths` should capture what the learner did well and should keep building on.
- `last_feedback_summary` should be a short summary in simple language accessible to a {native_language} speaker.
- Keep each list focused and short, usually 2 to 5 items.
- Return only structured data.
""".strip()


def build_profile_update_user_prompt(
    conversation: dict,
    user_messages: list[dict],
    final_feedback: dict,
    stored_feedback_items: list[dict],
) -> str:
    message_lines = []
    for message in user_messages:
        message_lines.append(f'Message ID: {message["id"]}\nText: {message["content"]}')

    feedback_lines = []
    for item in stored_feedback_items:
        mistakes = item.get("mistakes") or []
        explanations = item.get("explanations") or []
        feedback_lines.append(
            "\n".join(
                [
                    f'Message ID: {item["message_id"]}',
                    f'Original: {item["original_text"]}',
                    f'Corrected: {item["corrected_text"]}',
                    f"Mistakes: {_profile_value(mistakes)}",
                    f"Explanations: {_profile_value(explanations)}",
                ]
            )
        )

    overall_feedback = final_feedback.get("overall_feedback") or "No overall feedback provided."
    conversation_summary = conversation.get("conversation_summary") or "No stored conversation summary."

    return f"""
Update the learner profile after this completed conversation.

Conversation summary:
{conversation_summary}

Learner messages:
{"\n\n".join(message_lines) if message_lines else "No learner messages."}

Overall final feedback:
{overall_feedback}

Detailed message feedback:
{"\n\n".join(feedback_lines) if feedback_lines else "No detailed message feedback."}
""".strip()


def build_summary_text(messages: list[dict], *, limit: int = 8, chars_per_message: int = 180) -> str:
    recent_messages = messages[-limit:]
    summary_lines = []
    for item in recent_messages:
        speaker = "Learner" if item["sender"] == "user" else "Role"
        content = " ".join(item["content"].split())
        shortened = content[:chars_per_message]
        if len(content) > chars_per_message:
            shortened += "..."
        summary_lines.append(f"{speaker}: {shortened}")
    return "\n".join(summary_lines)
