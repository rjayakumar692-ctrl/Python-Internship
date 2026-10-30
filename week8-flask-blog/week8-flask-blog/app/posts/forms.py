from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    category = StringField('Category', validators=[Optional(), Length(max=50)])
    tags = StringField('Tags (comma separated)', validators=[Optional(), Length(max=200)])
    content = TextAreaField('Content (Markdown supported)', validators=[DataRequired()])
    image = FileField('Cover image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    published = BooleanField('Publish (untick to save as draft)', default=True)
    submit = SubmitField('Save post')
