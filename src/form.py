from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from . import db
from .model.user import User


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    firstname = StringField('First Name', validators=[Length(1, 10)])
    lastname = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])

    submit = SubmitField('Submit')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')


class ProjectForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Project Name', validators=[Length(1, 32)])
    comment = TextAreaField('Comment', validators=[Length(1, 1024)])
    submit = SubmitField('Create Project')


class SprintForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Sprint Name', validators=[Length(1, 32)])
    submit = SubmitField('Create Sprint')


class TaskForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Task Name', validators=[Length(1, 32)])
    description = TextAreaField('Sprint Description', validators=[Length(1, 1024)])
    submit = SubmitField('Add task to Sprint')
