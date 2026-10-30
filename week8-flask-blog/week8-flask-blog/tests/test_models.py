from app import db
from app.models import Comment, Post, User


def test_password_hashing(app):
    u = User(username='bob', email='bob@example.com')
    u.set_password('cat')
    assert u.password_hash != 'cat'
    assert u.check_password('cat')
    assert not u.check_password('dog')


def test_relationships_and_cascade(app):
    u = User(username='amy', email='amy@example.com')
    p = Post(title='T', content='C', author=u)
    c = Comment(content='Nice', author=u, post=p, approved=True)
    db.session.add_all([u, p, c])
    db.session.commit()
    assert u.posts.count() == 1
    assert p.approved_comment_count() == 1
    db.session.delete(p)
    db.session.commit()
    assert Comment.query.count() == 0


def test_tags(app):
    u = User(username='t', email='t@example.com')
    p = Post(title='T', content='C', author=u)
    p.set_tags('Flask, python, flask')
    db.session.add_all([u, p])
    db.session.commit()
    assert p.tag_string() == 'flask, python'
