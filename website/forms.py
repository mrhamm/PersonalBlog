from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Username',
    validators=[DataRequired()])

    password = PasswordField('Password',
    validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    search = StringField('Search for',validators=[DataRequired()])