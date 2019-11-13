from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
        title = StringField('Title', validators=[DataRequired()])
        picture = FileField('Upload Image', validators=[DataRequired(), FileAllowed(['jpg','png'])])
        submit = SubmitField('Post')