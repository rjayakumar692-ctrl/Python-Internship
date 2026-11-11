# Task Management REST API v1

Base URL: `http://127.0.0.1:5000/api/v1`

All protected endpoints require `Authorization: Bearer <access_token>`.

## Authentication
- `POST /auth/register` — `{ "username", "email", "password" }`; returns access and refresh tokens (201).
- `POST /auth/login` — `{ "email", "password" }`; returns tokens.
- `POST /auth/refresh` — refresh token required; returns a new access token.
- `POST /auth/password-reset` — `{ "email" }`; production deployments must deliver reset instructions by email.
- `POST /auth/password-reset/confirm` — reset-purpose token and `{ "password" }`.

## Users
- `GET /users/me` — current profile.
- `PATCH /users/me` — update `username` and/or `email`.
- `DELETE /users/me` — delete current account and owned tasks.

## Tasks
- `GET /tasks` — list own tasks. Query: `page`, `per_page` (1-100), `status`, `priority`, `category`, `search`, `sort_by` (`created_at`, `updated_at`, `due_date`, `priority`, `title`), `sort_order` (`asc`, `desc`).
- `POST /tasks` — create task. Fields: `title` (required, 3-160 chars), `description`, `status` (`pending`, `in_progress`, `completed`), `priority` (`low`, `medium`, `high`), `category`, `due_date` (`YYYY-MM-DD`), `assigned_to_id`.
- `GET /tasks/{id}` — task and comments.
- `PUT /tasks/{id}` — update task; title required.
- `PATCH /tasks/{id}` — partial update.
- `DELETE /tasks/{id}` — delete task.
- `POST /tasks/{id}/comments` — `{ "body": "..." }`.
- `DELETE /tasks/{id}/comments/{comment_id}` — delete own comment.

## Response format
Success: `{"status":"success","data":{...}}`
Error: `{"status":"error","message":"...","errors":{...}}`

Common status codes: 200 success, 201 created, 204 deleted, 400 validation error, 401 missing/invalid token, 404 missing resource, 409 duplicate account, 429 rate limit exceeded, 500 server error.

## Example
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"SecurePass123"}'
```

## Security notes
Use HTTPS in production, set strong secrets, store secrets outside source control, configure CORS narrowly, use a persistent rate-limit backend (Redis) for multi-worker deployments, and implement email delivery for password reset. The included development reset-token response is intentionally disabled unless Flask `DEBUG` is enabled.
