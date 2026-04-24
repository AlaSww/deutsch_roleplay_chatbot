# Flask Backend

This backend powers a German roleplay learning app. It exposes a JSON API for authentication, scenario discovery, roleplay conversations, inline message feedback, final conversation feedback, and learner profile updates.

This README is written as a UI handoff. A frontend engineer should be able to build the product flow from this document without reading the backend code first.

## Stack

- Flask app with blueprints
- PostgreSQL via `psycopg`
- JWT auth with Bearer tokens
- Groq for LLM responses and structured feedback generation
- OpenAPI JSON at `GET /openapi.json`
- Swagger UI at `GET /docs`

## Local setup

1. Create the database schema with `/database_ddl.sql`.
2. Seed sample data with `/app/seed_data.sql`.
3. Install dependencies:

```bash
pip install -r app/requirements.txt
```

4. Configure env vars in either `/.env` or `/app/.env`.
5. Run the server:

```bash
python -m app.run
```

Default local base URL is usually `http://localhost:5000`.

## Important env vars

- `DATABASE_URL` or `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT`
- `JWT_SECRET_KEY`
- `JWT_EXPIRES_IN_HOURS` default `24`
- `GROQ_API_KEY`
- `GROQ_CHAT_MODEL` default `llama-3.3-70b-versatile`
- `GROQ_STRUCTURED_MODEL` default `openai/gpt-oss-20b`
- `DEFAULT_OPENING_MESSAGE` default `true`
- `MAX_CONTEXT_MESSAGES` default `18`
- `SOFT_CONVERSATION_END_AFTER_USER_MESSAGES` default `6`
- `PORT` default `5000`

If `GROQ_API_KEY` is missing, conversation and feedback generation will fail.

## App structure

- [run.py](/home/ala/PROJECTS/python/german_scenario/app/run.py) starts the Flask app.
- [__init__.py](/home/ala/PROJECTS/python/german_scenario/app/__init__.py) registers the API and docs blueprints.
- [routes.py](/home/ala/PROJECTS/python/german_scenario/app/routes.py) contains all HTTP endpoints.
- [repositories.py](/home/ala/PROJECTS/python/german_scenario/app/repositories.py) contains database queries and response shaping.
- [services.py](/home/ala/PROJECTS/python/german_scenario/app/services.py) talks to Groq.
- [prompts.py](/home/ala/PROJECTS/python/german_scenario/app/prompts.py) builds roleplay, feedback, and profile update prompts.
- [docs.py](/home/ala/PROJECTS/python/german_scenario/app/docs.py) serves OpenAPI + Swagger UI.

## Core product model

The product revolves around these entities:

- `users`: auth identity, plan, German level, native language
- `user_profiles`: evolving learning profile used in prompts
- `scenarios`: roleplay situations like cafe visit or doctor appointment
- `scenario_roles`: exactly two roles per scenario in current product logic
- `conversations`: one user practicing one scenario as one selected role
- `messages`: alternating `user` and `assistant` messages
- `feedback_sessions`: overall feedback attached to a conversation
- `message_feedback`: correction details for individual user messages
- `conversation_summaries`: rolling summary used to limit long-context prompts

The database also has a `subscriptions` table, but this backend does not currently expose subscription endpoints or billing logic.

## Seeded demo data

Seeded users:

- `amina@example.com` / `amina123` / plan `free` / level `A1`
- `samir@example.com` / `samir123` / plan `free` / level `B1`
- `laura@example.com` / `laura123` / plan `premium` / level `C1`

Seeded scenarios:

- Cafe Visit
- Apartment Viewing
- Job Interview
- Doctor Appointment
- Train Station Help

Each scenario has two roles. Example: Cafe Visit has `Customer` and `Cafe Worker`.

## Authentication

Protected endpoints require:

```http
Authorization: Bearer <jwt>
```

Token behavior:

- token is returned by register and login
- token contains `sub`, `email`, `plan`, `iat`, `exp`
- expired or invalid tokens return `401`

Recommended UI behavior:

- store the JWT after login/register
- call `GET /api/auth/me` on app boot if a token exists
- if any protected request returns `401`, clear auth state and send user to login

## Public endpoints

- `GET /`
- `GET /docs`
- `GET /openapi.json`
- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/scenarios`
- `GET /api/scenarios/<scenario_id>`
- `GET /api/scenarios/<scenario_id>/roles`

## Protected endpoints

- `GET /api/auth/me`
- `GET /api/users`
- `GET /api/conversations`
- `POST /api/conversations`
- `GET /api/conversations/<conversation_id>`
- `POST /api/conversations/<conversation_id>/messages`
- `POST /api/conversations/<conversation_id>/messages/<message_id>/feedback`
- `GET /api/conversations/<conversation_id>/feedback`
- `POST /api/conversations/<conversation_id>/complete`

## Response conventions

- Success responses are plain JSON objects or arrays.
- Errors use:

```json
{ "error": "Human readable message" }
```

- UUIDs and timestamps are serialized as strings.
- There is no pagination anywhere right now.

## Main frontend screens

The current backend supports these UI surfaces cleanly:

1. Auth screens
2. Scenario list
3. Scenario detail / role picker
4. Conversation list
5. Active roleplay chat
6. Inline feedback for a specific learner message
7. Completed conversation feedback screen
8. Profile/progress screen based on `user_profile`

## End-to-end user flow

### 1. Register or login

Register:

```http
POST /api/auth/register
Content-Type: application/json
```

```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "plan": "free",
  "german_level": "A2",
  "native_language": "English",
  "common_mistakes": [],
  "grammar_focus_areas": [],
  "vocabulary_gaps": [],
  "strengths": [],
  "last_feedback_summary": null
}
```

Login:

```http
POST /api/auth/login
```

```json
{
  "email": "amina@example.com",
  "password": "amina123"
}
```

Both return:

```json
{
  "access_token": "jwt",
  "user": {
    "id": "uuid",
    "email": "amina@example.com",
    "plan": "free",
    "german_level": "A1",
    "native_language": "Arabic",
    "user_profile": {
      "id": "uuid",
      "user_id": "uuid",
      "common_mistakes": [],
      "grammar_focus_areas": [],
      "vocabulary_gaps": [],
      "strengths": [],
      "last_feedback_summary": null,
      "created_at": "timestamp",
      "updated_at": "timestamp"
    },
    "created_at": "timestamp"
  }
}
```

Validation notes:

- `password` must be at least 8 chars on register
- `plan` must be `free` or `premium`
- duplicate email returns `409`

### 2. Load scenarios

Use `GET /api/scenarios` for the main scenario chooser.

Each scenario already includes `roles`, so most UIs do not need an extra roles request:

```json
[
  {
    "id": "scenario-uuid",
    "name": "Cafe Visit",
    "description": "A conversation in a German cafe...",
    "prompt_context": "This roleplay happens in a busy but friendly cafe...",
    "is_premium": false,
    "created_at": "timestamp",
    "roles": [
      {
        "id": "role-uuid",
        "scenario_id": "scenario-uuid",
        "role_name": "Customer",
        "prompt_context": "You are the customer...",
        "created_at": "timestamp"
      },
      {
        "id": "role-uuid",
        "scenario_id": "scenario-uuid",
        "role_name": "Cafe Worker",
        "prompt_context": "You work in the cafe...",
        "created_at": "timestamp"
      }
    ]
  }
]
```

Use `GET /api/scenarios/<scenario_id>/roles` only if the UI wants to fetch roles separately.

Important product note:

- scenarios have an `is_premium` flag
- the backend currently does not enforce premium access
- if you want premium locking in the UI, you must implement it client-side for now

### 3. Create a conversation

```http
POST /api/conversations
Authorization: Bearer <jwt>
```

```json
{
  "scenario_id": "scenario-uuid",
  "scenario_role_id": "selected-role-uuid",
  "generate_opening_message": true
}
```

Behavior:

- user chooses one role
- AI automatically plays the other role
- backend expects the scenario to have exactly two roles
- response may already include the opening assistant message

The response is a conversation detail object. Important fields:

- `status`: starts as `active`
- `user_role_name`: the role selected by the learner
- `ai_role_name`: the opposite role
- `messages`: `[]` or one assistant opening message
- `feedback`: initially `null`
- `opening_message_error`: may exist if conversation was created but opening generation failed

UI recommendation:

- after create, navigate directly to the chat screen using the returned conversation payload
- if `opening_message_error` exists, show a non-blocking warning and let the learner start anyway

### 4. Active roleplay chat

Load conversation:

```http
GET /api/conversations/<conversation_id>
Authorization: Bearer <jwt>
```

This returns:

- conversation metadata
- scenario info
- role info
- learner profile snapshot used for prompts
- `messages`
- `feedback` if any exists
- `conversation_summary` if generated

Send a chat turn:

```http
POST /api/conversations/<conversation_id>/messages
Authorization: Bearer <jwt>
```

```json
{
  "content": "Ich moechte einen Kaffee und ein Croissant."
}
```

Success response:

```json
{
  "user_message": { "id": "uuid", "sender": "user", "content": "..." },
  "assistant_message": { "id": "uuid", "sender": "assistant", "content": "..." }
}
```

Chat notes:

- only active conversations accept new messages
- if conversation is completed, posting returns `400`
- after every successful turn, backend updates a rolling conversation summary
- `message_type`, `transcript`, and `audio_url` exist in the schema, but the current API only creates text messages

Failure case to handle carefully:

- if Groq fails, the endpoint returns `502`
- the response still includes the saved `user_message`
- that means the learner message is persisted even when no AI reply is generated

Example failure shape:

```json
{
  "error": "Groq API returned HTTP 500.",
  "user_message": { "id": "uuid", "sender": "user", "content": "..." }
}
```

UI implication:

- append the learner message locally
- show an error state for the missing assistant reply
- refresh conversation after retry if needed, because the user message already exists in storage

### 5. Inline feedback for one learner message

```http
POST /api/conversations/<conversation_id>/messages/<message_id>/feedback
Authorization: Bearer <jwt>
```

Only works for user messages, not assistant messages.

Response shape:

```json
{
  "feedback_session_id": "uuid",
  "feedback_summary": "Short summary",
  "message_feedback": {
    "id": "uuid",
    "feedback_session_id": "uuid",
    "message_id": "uuid",
    "original_text": "Ich bin gehen...",
    "corrected_text": "Ich gehe...",
    "mistakes": [
      {
        "span": "bin gehen",
        "issue": "Wrong verb form",
        "category": "grammar"
      }
    ],
    "better_alternatives": ["Ich gehe ..."],
    "explanations": ["Use the conjugated verb here."],
    "created_at": "timestamp"
  }
}
```

UI recommendation:

- treat this as on-demand feedback per message
- good fit for a "Check this message" action below learner bubbles
- if feedback is generated more than once for the same message, the backend updates the stored record

### 6. Complete the conversation

```http
POST /api/conversations/<conversation_id>/complete
Authorization: Bearer <jwt>
```

Rules:

- conversation must belong to the authenticated user
- conversation must have at least one user message
- backend marks conversation `completed`
- backend generates overall feedback plus per-message corrections
- backend then attempts to update `user_profile`

Response shape:

```json
{
  "feedback_session": {
    "id": "uuid",
    "conversation_id": "uuid",
    "overall_feedback": "Longer final summary",
    "created_at": "timestamp"
  },
  "message_feedback": [
    {
      "id": "uuid",
      "message_id": "uuid",
      "original_text": "...",
      "corrected_text": "...",
      "mistakes": [],
      "better_alternatives": [],
      "explanations": [],
      "created_at": "timestamp"
    }
  ],
  "user_profile": {
    "id": "uuid",
    "user_id": "uuid",
    "common_mistakes": [],
    "grammar_focus_areas": [],
    "vocabulary_gaps": [],
    "strengths": [],
    "last_feedback_summary": "...",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  },
  "profile_update_error": null,
  "final_feedback_error": null
}
```

Important nuance:

- if final feedback generation fails, backend tries a fallback assembled from single-message feedback
- in that fallback case, `final_feedback_error` can be non-null even though the endpoint still returns `200`
- `profile_update_error` can also be non-null while the feedback itself still succeeded

UI recommendation:

- show the final feedback page even if either error field is present
- surface those errors as small warnings, not fatal blockers

### 7. Load stored feedback later

```http
GET /api/conversations/<conversation_id>/feedback
Authorization: Bearer <jwt>
```

Returns the latest stored feedback session:

```json
{
  "id": "uuid",
  "conversation_id": "uuid",
  "overall_feedback": "Summary",
  "created_at": "timestamp",
  "message_feedback": [
    {
      "id": "uuid",
      "message_id": "uuid",
      "original_text": "...",
      "corrected_text": "...",
      "mistakes": [],
      "better_alternatives": [],
      "explanations": [],
      "created_at": "timestamp"
    }
  ]
}
```

If feedback has not been generated yet, this returns `404`.

### 8. Conversation history

`GET /api/conversations` returns past conversations for the authenticated user:

```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "scenario_id": "uuid",
    "scenario_role_id": "uuid",
    "status": "active",
    "started_at": "timestamp",
    "ended_at": null,
    "scenario_name": "Cafe Visit",
    "user_role_name": "Customer",
    "ai_role_name": "Cafe Worker"
  }
]
```

This is enough for a history list with:

- scenario title
- learner role
- AI role
- active/completed badge
- started date

## Useful UI mapping

### Scenario list card

Use:

- `name`
- `description`
- `is_premium`
- `roles[].role_name`

### Role selection screen

Use:

- `scenario.prompt_context` for expanded detail
- each role's `role_name`
- optionally a short trimmed version of `role.prompt_context`

### Chat header

Use:

- `scenario_name`
- `user_role_name`
- `ai_role_name`
- `status`

### Feedback UI

For each `message_feedback` item:

- `original_text` for what learner wrote
- `corrected_text` for suggested correction
- `mistakes[]` for highlighted issues
- `better_alternatives[]` for extra phrasing ideas
- `explanations[]` for teachable notes

### Profile/progress UI

Use `user.user_profile` or the `user_profile` returned from completion:

- `common_mistakes`
- `grammar_focus_areas`
- `vocabulary_gaps`
- `strengths`
- `last_feedback_summary`

## Access control and ownership rules

- scenario endpoints are public
- all conversation and feedback endpoints are private
- user can only access their own conversations
- unauthorized ownership access returns `403`
- some helper endpoints use `404` instead of exposing resource existence

One oddity:

- `GET /api/users` currently returns an array with only the authenticated user for backward compatibility
- most UIs should ignore this and use `GET /api/auth/me`

## Product constraints and quirks

These matter for frontend implementation:

- backend assumes exactly 2 roles per scenario
- backend keeps a learner message count and nudges the AI to wrap up naturally after `SOFT_CONVERSATION_END_AFTER_USER_MESSAGES`
- premium scenarios are flagged but not actually enforced server-side
- there is no refresh token flow
- there is no logout endpoint; logout is client-side token removal
- there is no pagination
- there is no websocket or streaming; chat is request/response
- there is no audio upload/generation endpoint even though message schema has `audio_url` and `transcript`
- there is no endpoint to edit or delete messages/conversations
- there is no endpoint to edit the learner profile directly from UI
- there is no CORS configuration in the app right now, so browser-based frontend hosting may need backend changes depending on deployment setup

## Suggested frontend state machine

Conversation statuses:

- `active`: learner can send messages and ask for inline feedback
- `completed`: learner can review final feedback, but cannot send new messages

Recommended client flow:

1. authenticate user
2. fetch scenarios
3. choose scenario and role
4. create conversation
5. render returned opening message if present
6. send user messages one turn at a time
7. optionally request per-message feedback
8. complete conversation
9. show final feedback and updated learner profile
10. allow reopening conversation detail as read-only history

## Error handling checklist

Handle these explicitly in the UI:

- `400` invalid UUID, missing fields, invalid state, wrong sender for feedback
- `401` missing/expired/invalid token
- `403` user does not own conversation
- `404` scenario, role, conversation, or feedback not found
- `409` duplicate email on registration
- `502` Groq or upstream generation failure

For `502` responses, show the server message from the `error` field.

## Recommended first implementation order for a UI

1. login/register
2. scenario list + role picker
3. create conversation
4. chat screen with turn sending
5. conversation history
6. final feedback screen
7. inline message feedback
8. profile/progress screen

## Quick API reference

- `GET /api/health`: liveness check
- `POST /api/auth/register`: create account and return JWT
- `POST /api/auth/login`: login and return JWT
- `GET /api/auth/me`: fetch current user
- `GET /api/scenarios`: list all scenarios with roles
- `GET /api/scenarios/<scenario_id>`: fetch one scenario
- `GET /api/scenarios/<scenario_id>/roles`: fetch only roles for one scenario
- `GET /api/conversations`: list current user's conversations
- `POST /api/conversations`: create a conversation
- `GET /api/conversations/<conversation_id>`: fetch conversation detail
- `POST /api/conversations/<conversation_id>/messages`: create user turn + AI turn
- `POST /api/conversations/<conversation_id>/messages/<message_id>/feedback`: generate feedback for one learner message
- `GET /api/conversations/<conversation_id>/feedback`: fetch stored final feedback
- `POST /api/conversations/<conversation_id>/complete`: finish conversation and generate final review

## Where to inspect exact schemas

- Swagger UI: `GET /docs`
- Raw OpenAPI spec: `GET /openapi.json`

For backend behavior details, the best source files are:

- [routes.py](/home/ala/PROJECTS/python/german_scenario/app/routes.py)
- [repositories.py](/home/ala/PROJECTS/python/german_scenario/app/repositories.py)
- [services.py](/home/ala/PROJECTS/python/german_scenario/app/services.py)
- [prompts.py](/home/ala/PROJECTS/python/german_scenario/app/prompts.py)
