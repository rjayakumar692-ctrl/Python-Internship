# Week 8 – Personal Blog with Flask

A full-featured blog: registration/login, post CRUD (Markdown editor), comments with
admin moderation + nested replies, categories & tags, image upload, search, pagination,
RSS feed, contact form, social sharing, tests and deployment notes.

## Tech stack
Flask · Flask-SQLAlchemy · Flask-Migrate · Flask-Login · Flask-WTF · SQLite · Jinja2 ·
Bootstrap 5 · EasyMDE (Markdown editor) · bleach (HTML sanitising) · pytest

## Quick start
```bash
python -m venv venv
venv\Scripts\activate          # Windows      |  source venv/bin/activate (macOS/Linux)
pip install -r requirements.txt

# create the database
set FLASK_APP=run.py           # Windows CMD  |  export FLASK_APP=run.py (macOS/Linux)
flask db init                  # only if migrations/ has no env.py yet
flask db migrate -m "initial tables"
flask db upgrade

flask seed                     # optional: admin/admin123 + sample posts
python run.py                  # http://127.0.0.1:5000
```
PowerShell: `$env:FLASK_APP="run.py"`.

**Admin:** the first account registered becomes admin (or run `flask make-admin <username>`).
Admins can moderate comments at `/comments/moderate` and edit/delete any post.

## Features → requirements map
| Requirement | Where |
|---|---|
| App factory + blueprints | `app/__init__.py`, `app/*/` |
| Auth (register/login/logout, hashing, profile) | `app/auth/` |
| Post CRUD, pagination, search, drafts | `app/posts/`, `app/main/routes.py` |
| Comments, moderation, nested replies | `app/comments/` |
| Categories, tags, image upload | `app/models.py`, `app/posts/` |
| RSS (`/feed.xml`), contact form, share buttons | `app/main/`, `templates/posts/detail.html` |
| Error pages 403/404/413/500 | `templates/errors/` |

## Security notes
CSRF protection on every form · passwords hashed (Werkzeug) · Markdown output sanitised with
bleach · open-redirect check on `?next=` · uploads renamed with UUIDs, 2 MB limit.
Set a strong `SECRET_KEY` in `.env` for production.

## Tests
```bash
pytest -v
```

## Deployment (PythonAnywhere)
1. Push to GitHub, then in a PythonAnywhere Bash console: `git clone <repo>`.
2. `mkvirtualenv blog --python=python3.10 && pip install -r requirements.txt`
3. Web tab → *Add new web app* → Manual config → set virtualenv path.
4. Edit the WSGI file:
   ```python
   import sys; sys.path.insert(0, '/home/<user>/week8-flask-blog')
   from run import app as application
   ```
5. Add env var `SECRET_KEY` in the WSGI file (or `.env`), run `flask db upgrade`, then *Reload*.
6. Static files: URL `/static/` → `/home/<user>/week8-flask-blog/app/static`.
7. HTTPS is free on the Web tab. **Backups:** schedule `python scripts/backup_db.py` in the Tasks tab.

Heroku: a `Procfile` is included (`gunicorn run:app`); use a Postgres add-on via `DATABASE_URL`
(Heroku's filesystem is ephemeral, so SQLite and uploads won't persist there).
