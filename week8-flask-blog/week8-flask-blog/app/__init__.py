import os
from datetime import datetime

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_class)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app import models  # noqa: F401  (registers models + user_loader)
    from app.utils import markdown_filter, excerpt_filter
    app.jinja_env.filters['markdown'] = markdown_filter
    app.jinja_env.filters['excerpt'] = excerpt_filter

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comments')

    @app.context_processor
    def inject_globals():
        return {'site_name': app.config['SITE_NAME'],
                'current_year': datetime.utcnow().year}

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def too_large_error(error):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': models.User, 'Post': models.Post,
                'Comment': models.Comment, 'Category': models.Category,
                'Tag': models.Tag}

    return app
