from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class CustomerPaymentForm(FlaskForm):

    payment_method = SelectField('Payment method *', validators=[DataRequired()])
    card_number = StringField('Card Number *', validators=[DataRequired()],
                              render_kw={"placeholder": "Enter your card number"})
    payment_method_details_csv = StringField('Csv *', validators=[DataRequired()])
    payment_method_details_month = SelectField('Month *', validators=[DataRequired()])
    payment_method_details_year = SelectField('Year *', validators=[DataRequired()])




