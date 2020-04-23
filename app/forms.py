from flask_wtf import FlaskForm 
from wtforms import BooleanField, SubmitField, StringField, PasswordField, SelectField, IntegerField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=30)])
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=10, message="Username must be between 4 and 10 characters long.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=30)])
    role = SelectField('Designation', validators=[DataRequired()], choices=[('Librarian', 'Librarian'), ('Faculty', 'Faculty'), ('Student', 'Student')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, message="Password should be atleast 4 characters long.")])
    confirm_pwd = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Should be same as the entered password.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose something else.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use. Please choose a different one.')


class LoginForm(FlaskForm):
    login_field = StringField('Username or Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountUpdation(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=30)])
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=10, message="Username must be between 4 and 10 characters long.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=30)])
    role = SelectField('Designation', validators=[DataRequired()], choices=[('Librarian', 'Librarian'), ('Faculty', 'Faculty'), ('Student', 'Student')])
    fine = IntegerField('Total Fine', validators=[DataRequired()])
    account_state = SelectField('Account Status', validators=[DataRequired()], choices=[('disabled', 'disabled'), ('enabled', 'enabled')])
    submit = SubmitField('Create Account')

class UpdateProfile(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=30)])
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=10, message="Username must be between 4 and 10 characters long.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=30)])
    role = StringField('Designation')
    fine = IntegerField('Total Fine')
    image_file = FileField('Update Profile Pic', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose something else.')

    def validate_email(self, email):
        if(email.data != current_user.email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use. Please choose a different one.')