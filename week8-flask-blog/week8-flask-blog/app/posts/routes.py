
from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.comments.forms import CommentForm
from app.models import Category, Comment, Post, Tag
from app.posts import bp
from app.posts.forms import PostForm
from app.utils import delete_image, save_image


def _can_manage(post):
    return current_user.is_authenticated and (
        current_user.id == post.user_id or current_user.is_admin
    )


def _apply_category(post, name):
    name = (name or '').strip()
    if not name:
        post.category = None
        return

    post.category = Category.query.filter(
        Category.name.ilike(name)
    ).first() or Category(name=name)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            published=form.published.data,
            author=current_user._get_current_object()
        )
        _apply_category(post, form.category.data)
        post.set_tags(form.tags.data)

        if form.image.data:
            post.image = save_image(form.image.data)

        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('posts.detail', post_id=post.id))

    return render_template(
        'posts/form.html',
        title='New post',
        form=form,
        heading='New post'
    )


@bp.route('/<int:post_id>')
def detail(post_id):
    post = db.get_or_404(Post, post_id)

    if not post.published and not _can_manage(post):
        abort(404)

    post.views = (post.views or 0) + 1
    db.session.commit()

    comments = (
        post.comments.filter_by(approved=True, parent_id=None)
        .order_by(Comment.timestamp.asc())
        .all()
    )

    return render_template(
        'posts/detail.html',
        title=post.title,
        post=post,
        comments=comments,
        form=CommentForm(),
        can_manage=_can_manage(post)
    )


@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = db.get_or_404(Post, post_id)

    if not _can_manage(post):
        abort(403)

    form = PostForm(obj=post) if request.method == 'GET' else PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.published = form.published.data
        _apply_category(post, form.category.data)
        post.set_tags(form.tags.data)

        if form.image.data:
            delete_image(post.image)
            post.image = save_image(form.image.data)

        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('posts.detail', post_id=post.id))

    if request.method == 'GET':
        form.category.data = post.category.name if post.category else ''
        form.tags.data = post.tag_string()

    return render_template(
        'posts/form.html',
        title='Edit post',
        form=form,
        heading='Edit post',
        post=post
    )


@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = db.get_or_404(Post, post_id)

    if not _can_manage(post):
        abort(403)

    delete_image(post.image)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')

    return redirect(url_for('main.index'))


def _listing(model_obj, endpoint, heading):
    page = request.args.get('page', 1, type=int)

    posts = (
        model_obj.posts.filter_by(published=True)
        .order_by(Post.timestamp.desc())
        .paginate(
            page=page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    )

    return render_template(
        'posts/list.html',
        title=heading,
        heading=heading,
        posts=posts,
        endpoint=endpoint,
        params={'name': model_obj.name}
    )


@bp.route('/category/<name>')
def category(name):
    return _listing(
        Category.query.filter_by(name=name).first_or_404(),
        'posts.category',
        f'Category: {name}'
    )


@bp.route('/tag/<name>')
def tag(name):
    return _listing(
        Tag.query.filter_by(name=name).first_or_404(),
        'posts.tag',
        f'Tagged: #{name}'
    )
