# UI

Production-oriented React frontend for the German roleplay backend.

## Stack

- React + TypeScript
- Vite
- Tailwind CSS
- TanStack Query
- React Router
- shadcn-inspired reusable component primitives

## Main routes

- `/`
- `/login`
- `/register`
- `/app/scenarios`
- `/app/scenarios/:scenarioId`
- `/app/history`
- `/app/profile`
- `/app/conversations/:conversationId`

## Run locally

```bash
npm install
npm run dev
```

The dev server proxies API requests to `http://127.0.0.1:5000`.

## Notes

- JWT is stored client-side and restored on boot through `/api/auth/me`.
- Premium scenario access is visually enforced in the UI only.
- Completed conversations are rendered read-only.
- The chat supports the backend case where a learner message is saved but AI reply generation fails with `502`.
