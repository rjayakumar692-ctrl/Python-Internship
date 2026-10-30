import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-me'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
    COMMENTS_PER_PAGE = 10
    SITE_NAME = 'My Personal Blog'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB upload limit
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret'
