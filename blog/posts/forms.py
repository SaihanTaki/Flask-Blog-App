from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,InputRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AddCommentForm(FlaskForm):
    comment = TextAreaField('Add a comment', validators=[InputRequired()])
    submit = SubmitField('submit')