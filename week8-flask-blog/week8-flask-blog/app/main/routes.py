from datetime import timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

from flask import Response, current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from app import db
from app.main import bp
from app.main.forms import ContactForm
from app.models import Category, Comment, ContactMessage, Post, Tag, User
from app.utils import excerpt_filter


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    query = Post.query.filter_by(published=True)
    if q:
        like = f'%{q}%'
        query = query.filter(Post.title.ilike(like) | Post.content.ilike(like))
    posts = query.order_by(
    Post.timestamp.desc(),
    Post.id.desc()
).paginate(
    page=page,
    per_page=current_app.config['POSTS_PER_PAGE'],
    error_out=False
)
    stats = {
        'posts': Post.query.filter_by(published=True).count(),
        'comments': Comment.query.filter_by(approved=True).count(),
        'categories': Category.query.count(),
    }
    popular = Post.query.filter_by(published=True).order_by(
    Post.views.desc(),
    Post.timestamp.desc(),
    Post.id.desc()
).limit(5).all()
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).limit(30).all()
    top_authors = (db.session.query(User, func.count(Post.id).label('n'))
                   .join(Post, Post.user_id == User.id).filter(Post.published.is_(True))
                   .group_by(User.id).order_by(func.count(Post.id).desc()).limit(3).all())
    return render_template('main/index.html', title='Home', posts=posts, q=q,
                           stats=stats, popular=popular, categories=categories,
                           tags=tags, top_authors=top_authors)


@bp.route('/about')
def about():
    return render_template('main/about.html', title='About')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        db.session.add(ContactMessage(name=form.name.data, email=form.email.data,
                                      message=form.message.data))
        db.session.commit()
        flash('Thanks! Your message has been received.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', title='Contact', form=form)


@bp.route('/feed.xml')
def feed():
    posts = Post.query.filter_by(published=True).order_by(Post.timestamp.desc()).limit(20).all()
    site = current_app.config['SITE_NAME']
    items = []
    for p in posts:
        link = url_for('posts.detail', post_id=p.id, _external=True)
        pub = format_datetime(p.timestamp.replace(tzinfo=timezone.utc))
        items.append(
            f'<item><title>{escape(p.title)}</title><link>{link}</link>'
            f'<guid>{link}</guid><pubDate>{pub}</pubDate>'
            f'<description>{escape(excerpt_filter(p.content, 300))}</description></item>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
           f'<title>{escape(site)}</title><link>{url_for("main.index", _external=True)}</link>'
           f'<description>Latest posts from {escape(site)}</description>'
           + ''.join(items) + '</channel></rss>')
    return Response(xml, mimetype='application/rss+xml')
