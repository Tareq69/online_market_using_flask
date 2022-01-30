from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators, ValidationError
from wtforms.validators import Length,EqualTo, Email, DataRequired
from market.models import *

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_address_to_check):
        email = User.query.filter_by(email=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')
    username = StringField(label="Username",validators=[Length(min=2, max=25)])
    email = StringField(label="Email",validators=[Email(),Length(min=2, max=25),DataRequired()])
    password1 = PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm Password",validators=[EqualTo('password1',message="Passwords do not match!"),DataRequired(),])
    submit = SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    username = StringField(label="Username",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField(label='Log in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')