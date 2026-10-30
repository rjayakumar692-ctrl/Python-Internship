from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.comments import bp
from app.comments.forms import CommentForm
from app.models import Comment, Post
from app.utils import admin_required


@bp.route('/add/<int:post_id>', methods=['POST'])
@login_required
def add(post_id):
    post = db.get_or_404(Post, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        parent = None
        if form.parent_id.data:
            parent = db.session.get(Comment, int(form.parent_id.data))
            if parent is None or parent.post_id != post.id:
                abort(400)
        # Admins and the post author are auto-approved; others wait for moderation.
        auto = current_user.is_admin or current_user.id == post.user_id
        comment = Comment(content=form.content.data, author=current_user._get_current_object(), post=post,
                          parent=parent, approved=auto)
        db.session.add(comment)
        db.session.commit()
        if auto:
            flash('Comment posted.', 'success')
        else:
            flash('Thanks! Your comment is awaiting moderation.', 'info')
    else:
        flash('Comment cannot be empty or longer than 1000 characters.', 'danger')
    return redirect(url_for('posts.detail', post_id=post.id) + '#comments')


@bp.route('/moderate')
@admin_required
def moderate():
    page = request.args.get('page', 1, type=int)
    pending = (Comment.query.filter_by(approved=False).order_by(Comment.timestamp.asc())
               .paginate(page=page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                         error_out=False))
    return render_template('comments/moderate.html', title='Moderate comments',
                           comments=pending)


@bp.route('/<int:comment_id>/approve', methods=['POST'])
@admin_required
def approve(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    comment.approved = True
    db.session.commit()
    flash('Comment approved.', 'success')
    return redirect(url_for('comments.moderate'))


@bp.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    if not (current_user.is_admin or current_user.id == comment.user_id):
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(request.referrer or url_for('posts.detail', post_id=post_id))
