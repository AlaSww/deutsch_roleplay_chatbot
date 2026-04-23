from __future__ import annotations

from typing import Any

from psycopg.types.json import Jsonb

from .db import execute, fetch_all, fetch_one


USER_PROFILE_FIELDS = (
    "common_mistakes",
    "grammar_focus_areas",
    "vocabulary_gaps",
    "strengths",
    "last_feedback_summary",
)
USER_PROFILE_ROW_KEYS = (
    "profile_id",
    "profile_user_id",
    "profile_created_at",
    "profile_updated_at",
    *USER_PROFILE_FIELDS,
)


def _default_user_profile() -> dict[str, Any]:
    return {
        "common_mistakes": [],
        "grammar_focus_areas": [],
        "vocabulary_gaps": [],
        "strengths": [],
        "last_feedback_summary": None,
    }


def _extract_user_profile(row: dict[str, Any]) -> dict[str, Any]:
    profile = {
        "id": row.get("profile_id"),
        "user_id": row.get("profile_user_id") or row.get("id"),
        "created_at": row.get("profile_created_at"),
        "updated_at": row.get("profile_updated_at"),
    }
    profile.update(_default_user_profile())
    for field in USER_PROFILE_FIELDS:
        value = row.get(field)
        if value is not None:
            profile[field] = value
    return profile


def _attach_user_profile(row: dict[str, Any]) -> dict[str, Any]:
    row["user_profile"] = _extract_user_profile(row)
    for key in USER_PROFILE_ROW_KEYS:
        row.pop(key, None)
    return row


def _jsonb(value: Any) -> Jsonb:
    return Jsonb(value)


def list_users() -> list[dict[str, Any]]:
    rows = fetch_all(
        """
        SELECT
            u.id,
            u.email,
            u.plan,
            u.german_level,
            u.native_language,
            u.created_at,
            up.id AS profile_id,
            up.user_id AS profile_user_id,
            up.common_mistakes,
            up.grammar_focus_areas,
            up.vocabulary_gaps,
            up.strengths,
            up.last_feedback_summary,
            up.created_at AS profile_created_at,
            up.updated_at AS profile_updated_at
        FROM public.users u
        LEFT JOIN public.user_profiles up ON up.user_id = u.id
        ORDER BY u.created_at ASC
        """
    )
    return [_attach_user_profile(row) for row in rows]


def get_user(user_id: str) -> dict[str, Any] | None:
    row = fetch_one(
        """
        SELECT
            u.id,
            u.email,
            u.plan,
            u.german_level,
            u.native_language,
            u.created_at,
            up.id AS profile_id,
            up.user_id AS profile_user_id,
            up.common_mistakes,
            up.grammar_focus_areas,
            up.vocabulary_gaps,
            up.strengths,
            up.last_feedback_summary,
            up.created_at AS profile_created_at,
            up.updated_at AS profile_updated_at
        FROM public.users u
        LEFT JOIN public.user_profiles up ON up.user_id = u.id
        WHERE u.id = %s
        """,
        (user_id,),
    )
    if not row:
        return None
    return _attach_user_profile(row)


def get_user_with_password_by_email(email: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, email, password_hash, plan, german_level, native_language, created_at
        FROM public.users
        WHERE email = %s
        """,
        (email,),
    )


def create_user(
    email: str,
    password_hash: str,
    german_level: str | None,
    native_language: str | None,
    plan: str,
    *,
    common_mistakes: list[Any] | None = None,
    grammar_focus_areas: list[Any] | None = None,
    vocabulary_gaps: list[Any] | None = None,
    strengths: list[Any] | None = None,
    last_feedback_summary: str | None = None,
) -> dict[str, Any]:
    row = execute(
        """
        WITH new_user AS (
            INSERT INTO public.users (
                email,
                password_hash,
                plan,
                german_level,
                native_language
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, email, plan, german_level, native_language, created_at
        )
        , new_profile AS (
            INSERT INTO public.user_profiles (
                user_id,
                common_mistakes,
                grammar_focus_areas,
                vocabulary_gaps,
                strengths,
                last_feedback_summary
            )
            SELECT
                id,
                %s,
                %s,
                %s,
                %s,
                %s
            FROM new_user
            RETURNING
                id AS profile_id,
                user_id AS profile_user_id,
                common_mistakes,
                grammar_focus_areas,
                vocabulary_gaps,
                strengths,
                last_feedback_summary,
                created_at AS profile_created_at,
                updated_at AS profile_updated_at
        )
        SELECT
            nu.id,
            nu.email,
            nu.plan,
            nu.german_level,
            nu.native_language,
            nu.created_at,
            np.profile_id,
            np.profile_user_id,
            np.common_mistakes,
            np.grammar_focus_areas,
            np.vocabulary_gaps,
            np.strengths,
            np.last_feedback_summary,
            np.profile_created_at,
            np.profile_updated_at
        FROM new_user nu
        JOIN new_profile np ON np.profile_user_id = nu.id
        """,
        (
            email,
            password_hash,
            plan,
            german_level,
            native_language,
            common_mistakes or [],
            grammar_focus_areas or [],
            vocabulary_gaps or [],
            strengths or [],
            last_feedback_summary,
        ),
        fetchone=True,
    )
    return _attach_user_profile(row)


def update_user_profile(
    user_id: str,
    *,
    common_mistakes: list[str],
    grammar_focus_areas: list[str],
    vocabulary_gaps: list[str],
    strengths: list[str],
    last_feedback_summary: str,
) -> dict[str, Any]:
    return execute(
        """
        UPDATE public.user_profiles
        SET common_mistakes = %s,
            grammar_focus_areas = %s,
            vocabulary_gaps = %s,
            strengths = %s,
            last_feedback_summary = %s,
            updated_at = NOW()
        WHERE user_id = %s
        RETURNING
            id,
            user_id,
            common_mistakes,
            grammar_focus_areas,
            vocabulary_gaps,
            strengths,
            last_feedback_summary,
            created_at,
            updated_at
        """,
        (
            _jsonb(common_mistakes),
            _jsonb(grammar_focus_areas),
            _jsonb(vocabulary_gaps),
            _jsonb(strengths),
            last_feedback_summary,
            user_id,
        ),
        fetchone=True,
    )


def list_scenarios() -> list[dict[str, Any]]:
    scenarios = fetch_all(
        """
        SELECT id, name, description, prompt_context, is_premium, created_at
        FROM public.scenarios
        ORDER BY created_at ASC, name ASC
        """
    )
    roles = fetch_all(
        """
        SELECT id, scenario_id, role_name, prompt_context, created_at
        FROM public.scenario_roles
        ORDER BY created_at ASC, role_name ASC
        """
    )

    roles_by_scenario: dict[str, list[dict[str, Any]]] = {}
    for role in roles:
        scenario_id = str(role["scenario_id"])
        roles_by_scenario.setdefault(scenario_id, []).append(role)

    for scenario in scenarios:
        scenario["roles"] = roles_by_scenario.get(str(scenario["id"]), [])

    return scenarios


def get_scenario(scenario_id: str) -> dict[str, Any] | None:
    scenario = fetch_one(
        """
        SELECT id, name, description, prompt_context, is_premium, created_at
        FROM public.scenarios
        WHERE id = %s
        """,
        (scenario_id,),
    )
    if not scenario:
        return None

    scenario["roles"] = fetch_all(
        """
        SELECT id, scenario_id, role_name, prompt_context, created_at
        FROM public.scenario_roles
        WHERE scenario_id = %s
        ORDER BY created_at ASC, role_name ASC
        """,
        (scenario_id,),
    )
    return scenario


def get_scenario_role(scenario_id: str, role_id: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT sr.id, sr.scenario_id, sr.role_name, sr.prompt_context
        FROM public.scenario_roles sr
        WHERE sr.id = %s
          AND sr.scenario_id = %s
        """,
        (role_id, scenario_id),
    )


def _get_other_scenario_role(scenario_id: str, selected_role_id: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT sr.id, sr.scenario_id, sr.role_name, sr.prompt_context
        FROM public.scenario_roles sr
        WHERE sr.scenario_id = %s
          AND sr.id <> %s
        ORDER BY sr.created_at ASC, sr.role_name ASC
        LIMIT 1
        """,
        (scenario_id, selected_role_id),
    )


def _attach_role_context(conversation: dict[str, Any]) -> dict[str, Any]:
    user_role = get_scenario_role(str(conversation["scenario_id"]), str(conversation["scenario_role_id"]))
    ai_role = _get_other_scenario_role(str(conversation["scenario_id"]), str(conversation["scenario_role_id"]))

    conversation["user_role"] = user_role
    conversation["ai_role"] = ai_role
    conversation["user_role_name"] = user_role["role_name"] if user_role else None
    conversation["user_role_prompt_context"] = user_role["prompt_context"] if user_role else None
    conversation["ai_role_name"] = ai_role["role_name"] if ai_role else None
    conversation["ai_role_prompt_context"] = ai_role["prompt_context"] if ai_role else None
    return conversation


def create_conversation(user_id: str, scenario_id: str, scenario_role_id: str) -> dict[str, Any]:
    return execute(
        """
        INSERT INTO public.conversations (
            user_id,
            scenario_id,
            scenario_role_id
        )
        VALUES (%s, %s, %s)
        RETURNING id, user_id, scenario_id, scenario_role_id, status, started_at, ended_at
        """,
        (user_id, scenario_id, scenario_role_id),
        fetchone=True,
    )


def list_conversations(user_id: str | None = None) -> list[dict[str, Any]]:
    if user_id:
        conversations = fetch_all(
            """
            SELECT
                c.id,
                c.user_id,
                c.scenario_id,
                c.scenario_role_id,
                c.status,
                c.started_at,
                c.ended_at,
                s.name AS scenario_name,
                sr.role_name AS user_role_name
            FROM public.conversations c
            JOIN public.scenarios s ON s.id = c.scenario_id
            JOIN public.scenario_roles sr ON sr.id = c.scenario_role_id
            WHERE c.user_id = %s
            ORDER BY c.started_at DESC
            """,
            (user_id,),
        )
    else:
        conversations = fetch_all(
        """
        SELECT
            c.id,
            c.user_id,
            c.scenario_id,
            c.scenario_role_id,
            c.status,
            c.started_at,
            c.ended_at,
            s.name AS scenario_name,
            sr.role_name AS user_role_name
        FROM public.conversations c
        JOIN public.scenarios s ON s.id = c.scenario_id
        JOIN public.scenario_roles sr ON sr.id = c.scenario_role_id
        ORDER BY c.started_at DESC
        """
        )

    for conversation in conversations:
        ai_role = _get_other_scenario_role(str(conversation["scenario_id"]), str(conversation["scenario_role_id"]))
        conversation["ai_role_name"] = ai_role["role_name"] if ai_role else None

    return conversations


def get_conversation(conversation_id: str) -> dict[str, Any] | None:
    conversation = fetch_one(
        """
        SELECT
            c.id,
            c.user_id,
            c.scenario_id,
            c.scenario_role_id,
            c.status,
            c.started_at,
            c.ended_at,
            u.email,
            u.plan AS user_plan,
            u.german_level,
            u.native_language,
            up.id AS profile_id,
            up.user_id AS profile_user_id,
            up.common_mistakes,
            up.grammar_focus_areas,
            up.vocabulary_gaps,
            up.strengths,
            up.last_feedback_summary,
            up.created_at AS profile_created_at,
            up.updated_at AS profile_updated_at,
            s.name AS scenario_name,
            s.description AS scenario_description,
            s.prompt_context AS scenario_prompt_context,
            s.is_premium,
            cs.summary AS conversation_summary,
            cs.updated_at AS summary_updated_at
        FROM public.conversations c
        JOIN public.users u ON u.id = c.user_id
        LEFT JOIN public.user_profiles up ON up.user_id = u.id
        JOIN public.scenarios s ON s.id = c.scenario_id
        LEFT JOIN LATERAL (
            SELECT summary, updated_at
            FROM public.conversation_summaries
            WHERE conversation_id = c.id
            ORDER BY updated_at DESC
            LIMIT 1
        ) cs ON TRUE
        WHERE c.id = %s
        """,
        (conversation_id,),
    )
    if not conversation:
        return None
    _attach_user_profile(conversation)
    return _attach_role_context(conversation)


def create_message(
    conversation_id: str,
    sender: str,
    content: str,
    *,
    message_type: str = "text",
    transcript: str | None = None,
    audio_url: str | None = None,
) -> dict[str, Any]:
    return execute(
        """
        INSERT INTO public.messages (
            conversation_id,
            sender,
            message_type,
            content,
            transcript,
            audio_url
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, conversation_id, sender, message_type, content, transcript, audio_url, created_at
        """,
        (conversation_id, sender, message_type, content, transcript, audio_url),
        fetchone=True,
    )


def list_messages(conversation_id: str) -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT id, conversation_id, sender, message_type, content, transcript, audio_url, created_at
        FROM public.messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC
        """,
        (conversation_id,),
    )


def get_message(conversation_id: str, message_id: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, conversation_id, sender, message_type, content, transcript, audio_url, created_at
        FROM public.messages
        WHERE conversation_id = %s
          AND id = %s
        """,
        (conversation_id, message_id),
    )


def get_or_create_feedback_session(conversation_id: str) -> dict[str, Any]:
    session = fetch_one(
        """
        SELECT id, conversation_id, overall_feedback, created_at
        FROM public.feedback_sessions
        WHERE conversation_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (conversation_id,),
    )
    if session:
        return session

    return execute(
        """
        INSERT INTO public.feedback_sessions (
            conversation_id
        )
        VALUES (%s)
        RETURNING id, conversation_id, overall_feedback, created_at
        """,
        (conversation_id,),
        fetchone=True,
    )


def update_feedback_session(session_id: str, overall_feedback: str) -> dict[str, Any]:
    return execute(
        """
        UPDATE public.feedback_sessions
        SET overall_feedback = %s
        WHERE id = %s
        RETURNING id, conversation_id, overall_feedback, created_at
        """,
        (overall_feedback, session_id),
        fetchone=True,
    )


def get_message_feedback_by_message(message_id: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT
            id,
            feedback_session_id,
            message_id,
            original_text,
            corrected_text,
            mistakes,
            better_alternatives,
            explanations,
            created_at
        FROM public.message_feedback
        WHERE message_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (message_id,),
    )


def upsert_message_feedback(
    feedback_session_id: str,
    message_id: str,
    original_text: str,
    corrected_text: str,
    mistakes: list[dict[str, Any]],
    better_alternatives: list[str],
    explanations: list[str],
) -> dict[str, Any]:
    existing = get_message_feedback_by_message(message_id)
    if existing:
        return execute(
            """
            UPDATE public.message_feedback
            SET feedback_session_id = %s,
                original_text = %s,
                corrected_text = %s,
                mistakes = %s,
                better_alternatives = %s,
                explanations = %s,
                created_at = NOW()
            WHERE id = %s
            RETURNING id, feedback_session_id, message_id, original_text, corrected_text,
                      mistakes, better_alternatives, explanations, created_at
            """,
            (
                feedback_session_id,
                original_text,
                corrected_text,
                _jsonb(mistakes),
                _jsonb(better_alternatives),
                _jsonb(explanations),
                existing["id"],
            ),
            fetchone=True,
        )

    return execute(
        """
        INSERT INTO public.message_feedback (
            feedback_session_id,
            message_id,
            original_text,
            corrected_text,
            mistakes,
            better_alternatives,
            explanations
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, feedback_session_id, message_id, original_text, corrected_text,
                  mistakes, better_alternatives, explanations, created_at
        """,
        (
            feedback_session_id,
            message_id,
            original_text,
            corrected_text,
            _jsonb(mistakes),
            _jsonb(better_alternatives),
            _jsonb(explanations),
        ),
        fetchone=True,
    )


def list_feedback_for_conversation(conversation_id: str) -> dict[str, Any] | None:
    session = fetch_one(
        """
        SELECT id, conversation_id, overall_feedback, created_at
        FROM public.feedback_sessions
        WHERE conversation_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (conversation_id,),
    )
    if not session:
        return None

    session["message_feedback"] = fetch_all(
        """
        SELECT
            mf.id,
            mf.feedback_session_id,
            mf.message_id,
            mf.original_text,
            mf.corrected_text,
            mf.mistakes,
            mf.better_alternatives,
            mf.explanations,
            mf.created_at
        FROM public.message_feedback mf
        WHERE mf.feedback_session_id = %s
        ORDER BY mf.created_at ASC
        """,
        (session["id"],),
    )
    return session


def upsert_conversation_summary(conversation_id: str, summary: str) -> dict[str, Any]:
    existing = fetch_one(
        """
        SELECT id
        FROM public.conversation_summaries
        WHERE conversation_id = %s
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        (conversation_id,),
    )
    if existing:
        return execute(
            """
            UPDATE public.conversation_summaries
            SET summary = %s,
                updated_at = NOW()
            WHERE id = %s
            RETURNING id, conversation_id, summary, updated_at
            """,
            (summary, existing["id"]),
            fetchone=True,
        )

    return execute(
        """
        INSERT INTO public.conversation_summaries (
            conversation_id,
            summary
        )
        VALUES (%s, %s)
        RETURNING id, conversation_id, summary, updated_at
        """,
        (conversation_id, summary),
        fetchone=True,
    )


def complete_conversation(conversation_id: str) -> dict[str, Any]:
    return execute(
        """
        UPDATE public.conversations
        SET status = 'completed',
            ended_at = NOW()
        WHERE id = %s
        RETURNING id, user_id, scenario_id, scenario_role_id, status, started_at, ended_at
        """,
        (conversation_id,),
        fetchone=True,
    )
