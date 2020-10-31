from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from  wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
import email_validator
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User
from flask_login import current_user


class Registrationform(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Passsword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user  =User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("The username has been already used. Please choose different one")

    def validate_email(self, email):
        user  =User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("The Email has been already used. Please choose different one")



class Userupdateform(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user  =User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("The username already exist. Please choose different one")

    def validate_email(self, email):
        if email.data != current_user.email:
            user  =User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("The Email has been already used. Please choose different one")






class Loginform(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ResetEmailform(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = User.query.filter_by('email').first()
        if user is None:
            ValidationError('The user with this email donot exist')   


class Resetpasswordform(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpasssword = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


    