import click
from app import create_app, db
from app.models import User, Post, Category, Tag

app = create_app()


@app.cli.command('seed')
def seed():
    """Create an admin user and sample posts: flask seed"""
    if User.query.filter_by(username='admin').first():
        click.echo('Already seeded.')
        return
    admin = User(username='admin', email='admin@example.com', is_admin=True,
                 about_me='Blog owner.')
    admin.set_password('admin123')
    db.session.add(admin)
    cat = Category(name='Web Development')
    db.session.add(cat)
    for i in range(1, 4):
        p = Post(title=f'Sample post {i}', author=admin, category=cat,
                 content='## Hello\n\nThis is **sample** content written in Markdown.')
        p.set_tags('flask, python')
        db.session.add(p)
    db.session.commit()
    click.echo('Seeded. Login: admin / admin123 (change the password!)')


@app.cli.command('make-admin')
@click.argument('username')
def make_admin(username):
    """Promote a user to admin: flask make-admin <username>"""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo('User not found.')
        return
    user.is_admin = True
    db.session.commit()
    click.echo(f'{username} is now an admin.')


if __name__ == '__main__':
    app.run(debug=True)
