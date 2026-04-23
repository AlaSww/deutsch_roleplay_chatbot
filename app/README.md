# Flask Backend

This folder contains the backend API for the German roleplay app.

## What it does

- Supports JWT authentication with password-based login and registration.
- Stores learner profile details in `user_profiles` and includes them in LLM prompts.
- Lists seeded scenarios and their two available roles.
- Starts roleplay conversations where the user chooses one role and the AI plays the other.
- Uses Groq to generate in-character replies.
- Generates inline feedback for one learner message during an active conversation.
- Generates final overall feedback plus per-message corrections when a conversation ends.
- Exposes Swagger UI documentation for local testing.

## Setup

1. Create the database schema with `/database_ddl.sql`.
2. Insert sample data with `/app/seed_data.sql`.
   The seed file is idempotent and updates the predefined users, user profiles, scenarios, and roles if you rerun it.
3. Install dependencies:

```bash
pip install -r app/requirements.txt
```

4. Copy `app/.env.example` to your own environment file and set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `JWT_SECRET_KEY`, and `GROQ_API_KEY`.
5. Run the server:

```bash
python -m app.run
```

## Main endpoints

- `GET /docs`
- `GET /openapi.json`
- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/users`
- `GET /api/scenarios`
- `GET /api/scenarios/<scenario_id>`
- `GET /api/conversations`
- `POST /api/conversations`
- `GET /api/conversations/<conversation_id>`
- `POST /api/conversations/<conversation_id>/messages`
- `POST /api/conversations/<conversation_id>/messages/<message_id>/feedback`
- `GET /api/conversations/<conversation_id>/feedback`
- `POST /api/conversations/<conversation_id>/complete`

## Important note

Most user-specific endpoints require `Authorization: Bearer <jwt>`. The seeded demo users can log in with:

- `amina@example.com` / `amina123`
- `samir@example.com` / `samir123`
- `laura@example.com` / `laura123`
