from app import db
from app.models import Comment, Post
from tests.conftest import login, register


def make_post(client, title='Hello World', **extra):
    data = {'title': title, 'content': 'Some **markdown** content',
            'category': 'Tech', 'tags': 'flask, python', 'published': 'y'}
    data.update(extra)
    return client.post('/posts/create', data=data, follow_redirects=True)


def test_home_and_404(client):
    assert client.get('/').status_code == 200
    assert client.get('/nope').status_code == 404


def test_register_login_logout(client):
    r = register(client, 'alice')
    assert b'Registration successful' in r.data
    assert b'Invalid username or password' in login(client, 'alice', 'wrong').data
    assert b'alice' in login(client, 'alice').data
    assert b'logged out' in client.post('/auth/logout', follow_redirects=True).data


def test_register_validation(client):
    register(client, 'alice')
    r = register(client, 'alice')
    assert b'taken' in r.data


def test_login_required(client):
    r = client.get('/posts/create')
    assert r.status_code == 302 and '/auth/login' in r.headers['Location']


def test_post_crud(client, app):
    register(client, 'alice')
    login(client, 'alice')
    r = make_post(client)
    assert b'Hello World' in r.data and b'<strong>markdown</strong>' in r.data
    post = Post.query.first()
    r = client.post(f'/posts/{post.id}/edit', data={
        'title': 'Updated', 'content': 'new', 'published': 'y'}, follow_redirects=True)
    assert b'Updated' in r.data
    r = client.post(f'/posts/{post.id}/delete', follow_redirects=True)
    assert b'Post deleted' in r.data and Post.query.count() == 0


def test_xss_is_sanitised(client):
    register(client, 'alice')
    login(client, 'alice')
    r = make_post(client, content='<script>alert(1)</script>hi')
    assert b'<script>alert(1)</script>' not in r.data


def test_search_and_pagination(client, app):
    register(client, 'alice')
    login(client, 'alice')
    for i in range(7):
        make_post(client, title=f'Post number {i}')
    assert b'Post number 6' in client.get('/').data
    assert b'Post number 0' not in client.get('/').data      # on page 2
    assert b'Post number 0' in client.get('/?page=2').data
    assert b'Post number 3' in client.get('/?q=number 3').data


def test_other_user_cannot_edit(client):
    register(client, 'alice')       # admin (first user)
    register(client, 'bob')
    login(client, 'alice')
    make_post(client)
    client.post('/auth/logout')
    login(client, 'bob')
    assert client.get('/posts/1/edit').status_code == 403


def test_comment_moderation(client):
    register(client, 'alice')       # admin
    register(client, 'bob')
    login(client, 'alice')
    make_post(client)
    client.post('/auth/logout')
    login(client, 'bob')
    r = client.post('/comments/add/1', data={'content': 'Great post'}, follow_redirects=True)
    assert b'awaiting moderation' in r.data
    assert b'Great post' not in client.get('/posts/1').data
    assert client.get('/comments/moderate').status_code == 403
    client.post('/auth/logout')
    login(client, 'alice')
    assert b'Great post' in client.get('/comments/moderate').data
    client.post(f'/comments/{Comment.query.first().id}/approve')
    assert b'Great post' in client.get('/posts/1').data


def test_rss_and_contact(client):
    assert client.get('/feed.xml').mimetype == 'application/rss+xml'
    r = client.post('/contact', data={'name': 'A', 'email': 'a@b.com',
                                      'message': 'Hello there!'}, follow_redirects=True)
    assert b'message has been received' in r.data
