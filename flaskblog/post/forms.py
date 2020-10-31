from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from  wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf.file import FileField, FileAllowed

class Createpost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    genere = StringField('Genere', validators=[DataRequired(), Length(min=5, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    blog_pic = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

   
