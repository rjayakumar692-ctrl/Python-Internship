import os
import uuid
from functools import wraps
from urllib.parse import urlparse

import bleach
import markdown
from flask import abort, current_app
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import secure_filename

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    'p', 'pre', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img',
    'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'span']
ALLOWED_ATTRS = {**bleach.sanitizer.ALLOWED_ATTRIBUTES,
                 'img': ['src', 'alt', 'title'], 'code': ['class']}


def markdown_filter(text):
    """Markdown -> sanitised HTML (safe against XSS)."""
    html = markdown.markdown(text or '', extensions=['fenced_code', 'tables', 'nl2br'])
    return Markup(bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS))


def excerpt_filter(text, length=220):
    html = markdown.markdown(text or '')
    plain = bleach.clean(html, tags=[], strip=True).strip()
    return plain if len(plain) <= length else plain[:length].rsplit(' ', 1)[0] + '…'


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper


def save_image(file_storage):
    """Save an uploaded image with a random name; return the filename."""
    ext = os.path.splitext(secure_filename(file_storage.filename))[1].lower()
    filename = f'{uuid.uuid4().hex}{ext}'
    file_storage.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return filename


def delete_image(filename):
    if filename:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(path):
            os.remove(path)


def is_safe_url(target):
    return bool(target) and not urlparse(target).netloc and target.startswith('/')
