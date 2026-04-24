# German Scenario

AI-powered German roleplay practice app with:

- a Flask backend
- a React + TypeScript frontend
- PostgreSQL storage
- Groq-based roleplay and feedback generation

The product is designed around realistic conversations. A learner chooses a scenario, picks one of the two roles, chats with the AI in German, requests inline feedback when needed, and ends the session with a full review plus an updated learner profile.

## What The App Does

- Authentication with JWT
- Public scenario discovery
- Role-based conversation setup
- AI-generated in-character chat replies
- On-demand feedback for a single learner message
- Final conversation feedback with message-by-message corrections
- Learner profile tracking over time
- Conversation history and read-only review of completed sessions

## Example Product Flow

1. Sign up or log in
2. Browse scenarios like:
   - Cafe Visit
   - Apartment Viewing
   - Job Interview
   - Customer Complaint Resolution
   - Performance Review
3. Choose one role
4. Start the conversation
5. Chat with the AI in German
6. Request inline feedback on learner messages
7. Complete the conversation
8. Review final feedback and updated learning insights

## Project Structure

```text
.
├── app/                Flask backend
├── ui/                 React frontend
├── database_ddl.sql    PostgreSQL schema
└── README.md
```

Important files:

- [database_ddl.sql](/home/ala/PROJECTS/python/german_scenario/database_ddl.sql): database schema
- [app/seed_data.sql](/home/ala/PROJECTS/python/german_scenario/app/seed_data.sql): demo users, scenarios, and roles
- [app/README.md](/home/ala/PROJECTS/python/german_scenario/app/README.md): backend/API details
- [ui/README.md](/home/ala/PROJECTS/python/german_scenario/ui/README.md): frontend details

## Tech Stack

### Backend

- Flask
- psycopg
- PostgreSQL
- PyJWT
- Groq API

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query
- React Router

## Core Domain Model

- `users`: account identity and learner settings
- `user_profiles`: strengths, grammar focus areas, vocabulary gaps, recurring mistakes
- `scenarios`: roleplay situations
- `scenario_roles`: exactly two roles per scenario
- `conversations`: one learner in one scenario with one chosen role
- `messages`: learner and assistant turns
- `feedback_sessions`: final conversation review
- `message_feedback`: detailed corrections per learner message
- `conversation_summaries`: compact context for longer chats

## Seeded Data

The seed file includes:

- 3 demo users
- beginner, intermediate, and advanced learner profiles
- 25 scenarios total
- both everyday and professional roleplay situations

Demo users:

- `amina@example.com` / `amina123`
- `samir@example.com` / `samir123`
- `laura@example.com` / `laura123`

## Professional Scenarios Included

The project includes a broad set of workplace-focused scenarios, for example:

- Team Meeting Update
- Client Kickoff Call
- Performance Review
- Salary Negotiation
- Technical Support Ticket
- Product Demo
- Vendor Negotiation
- Marketing Campaign Planning
- Contract Review Discussion
- Office Conflict Mediation
- Board Presentation Preparation

These are meant to maximize practical German for work, meetings, interviews, negotiation, support, and business communication.

## Backend Behavior

Important product rules implemented in the backend:

- scenario routes are public
- conversation and feedback routes require JWT auth
- each scenario is expected to have exactly 2 roles
- completed conversations are read-only
- premium scenarios are flagged in the data, but not enforced server-side
- the AI is nudged to wrap up naturally after a soft threshold instead of being hard-stopped by a message cap
- inline feedback only works on learner messages

## Frontend Behavior

The UI includes:

- landing page
- login/register pages
- scenario browser with filtering
- scenario detail and role selection
- active chat screen
- inline message feedback
- final feedback review
- history page
- learner progress/profile page

The frontend stores the JWT locally and restores the session by calling `/api/auth/me` on boot.

## Local Setup

### 1. Create the database

Run the schema in PostgreSQL:

```bash
psql -d german_scenario -f database_ddl.sql
```

Then seed demo data:

```bash
psql -d german_scenario -f app/seed_data.sql
```

### 2. Configure backend environment

Copy and edit:

```bash
cp app/.env.example app/.env
```

Required values include:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `JWT_SECRET_KEY`
- `GROQ_API_KEY`

### 3. Run the backend

```bash
pip install -r app/requirements.txt
python -m app.run
```

Default backend URL:

```text
http://127.0.0.1:5000
```

### 4. Run the frontend

```bash
cd ui
npm install
npm run dev
```

Default frontend URL:

```text
http://127.0.0.1:5173
```

The Vite dev server proxies `/api`, `/docs`, and `/openapi.json` to the Flask app.

## Main API Endpoints

### Public

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/scenarios`
- `GET /api/scenarios/<scenario_id>`
- `GET /api/scenarios/<scenario_id>/roles`

### Protected

- `GET /api/auth/me`
- `GET /api/conversations`
- `POST /api/conversations`
- `GET /api/conversations/<conversation_id>`
- `POST /api/conversations/<conversation_id>/messages`
- `POST /api/conversations/<conversation_id>/messages/<message_id>/feedback`
- `GET /api/conversations/<conversation_id>/feedback`
- `POST /api/conversations/<conversation_id>/complete`

## Useful Dev URLs

- Backend root: `GET /`
- Swagger UI: `GET /docs`
- OpenAPI JSON: `GET /openapi.json`

## Error Handling Notes

The app is built around these common backend responses:

- `400` invalid input or invalid conversation state
- `401` invalid or expired JWT
- `403` ownership/access issue
- `404` missing resource
- `409` duplicate email during registration
- `502` AI generation failed

Special case:

- when a chat reply fails with `502`, the learner message may still already be saved
- the frontend is expected to show that message and allow the user to continue or refresh

## Documentation

For deeper details:

- Backend/API documentation: [app/README.md](/home/ala/PROJECTS/python/german_scenario/app/README.md)
- Frontend documentation: [ui/README.md](/home/ala/PROJECTS/python/german_scenario/ui/README.md)

## Current Scope / Limitations

- no streaming chat
- no audio upload/generation flow yet
- no message edit/delete flow
- no direct learner profile editing UI
- no server-enforced premium access yet
- no refresh token flow

## Development Notes

- `.env` files and `node_modules` are ignored via [`.gitignore`](/home/ala/PROJECTS/python/german_scenario/.gitignore)
- the seed file is idempotent and safe to rerun
- the backend and frontend are structured separately so each can evolve independently

## Recommended Start Point

If you want to understand the project quickly:

1. Read this README
2. Read [app/README.md](/home/ala/PROJECTS/python/german_scenario/app/README.md)
3. Run the backend
4. Run the frontend
5. Log in with a demo account
6. Start a scenario and go through a full conversation cycle
