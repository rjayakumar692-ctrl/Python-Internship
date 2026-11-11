# Week 9 — Task Management REST API

A Flask REST API featuring JWT authentication, user profiles, task CRUD, filtering, sorting, pagination, task comments, validation, rate limiting, CORS, migrations, tests, OpenAPI and Postman assets.

## 1. Setup (Windows PowerShell)
```powershell
cd week9-task-api
py -3 -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and replace both secret values with long random strings.

## 2. Database
```powershell
flask --app run.py db init
flask --app run.py db migrate -m "Initial tables"
flask --app run.py db upgrade
```
For a quick local-only start without migrations, run `flask --app run.py init-db`.

## 3. Run
```powershell
python run.py
```
Health check: `http://127.0.0.1:5000/health`

## 4. Test
```powershell
pytest -v
```

## 5. Postman
Import `docs/postman_collection.json`. Register or login first, then copy the `access_token` from the response into the collection's `access_token` variable.

## 6. API reference
Read `docs/api.md` or import `docs/swagger.yaml` into Swagger Editor/Postman.

## Important implementation notes
- Task list and detail operations are scoped to the authenticated task owner.
- Task assignment stores an assignee ID; it does not grant that assignee ownership or read access.
- Password reset is a development-ready stub: production must send a short-lived, single-use reset token through email. Never expose reset tokens in production.
- For production, use HTTPS, strong secrets, Redis-backed rate limiting, email verification/reset delivery, and a managed database.
