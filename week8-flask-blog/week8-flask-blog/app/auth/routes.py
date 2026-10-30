from datetime import datetime

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.auth import bp
from app.auth.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Post, User
from app.utils import is_safe_url


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        user.is_admin = User.query.count() == 0  # first user becomes admin
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        user.last_seen = datetime.utcnow()
        db.session.commit()
        next_page = request.args.get('next')
        return redirect(next_page if is_safe_url(next_page) else url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    query = user.posts.order_by(Post.timestamp.desc())
    if not (current_user.is_authenticated and
            (current_user.id == user.id or current_user.is_admin)):
        query = query.filter_by(published=True)
    posts = query.paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'],
                           error_out=False)
    return render_template('auth/profile.html', title=user.username, user=user, posts=posts)


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('auth.profile', username=current_user.username))
    return render_template('auth/edit_profile.html', title='Edit profile', form=form)
