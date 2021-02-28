from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, IntegerField


class ProfileForm(FlaskForm):
    first_name = StringField('First Name *', validators=[DataRequired()], render_kw={"placeholder": "Enter your first name"})
    last_name = StringField('Last Name *', validators=[DataRequired()], render_kw={"placeholder": "Enter your last name"})
    email = EmailField('Email address *', validators=[DataRequired()], render_kw={"placeholder": "Enter your email"})
    address = StringField('Address', validators=[], render_kw={"placeholder": "Enter your address"})
    phone_number = IntegerField('Phone number', validators=[DataRequired()], render_kw={"placeholder": "Enter your phone number"})
    username = StringField('Username *', validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[], render_kw={"placeholder": "Enter your password"})
    r_password = PasswordField('Repeat Password', validators=[], render_kw={"placeholder": "Repeat your password"})

