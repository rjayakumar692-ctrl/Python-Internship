from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class CommentForm(FlaskForm):
    content = TextAreaField('Your comment', validators=[DataRequired(), Length(1, 1000)])
    parent_id = HiddenField(validators=[Optional()])
    submit = SubmitField('Post comment')
