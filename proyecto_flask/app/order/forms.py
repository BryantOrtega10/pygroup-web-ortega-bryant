from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class CompleteOrderForm(FlaskForm):
    address = StringField('Shipping Address *', validators=[DataRequired()], render_kw={"placeholder": "Enter your address"})
    payment_method = SelectField('Payment method *', validators=[DataRequired()])
