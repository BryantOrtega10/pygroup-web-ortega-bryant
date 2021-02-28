from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired


class CreateCategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class CreateProductForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    refundable = RadioField('Refundable', validators=[], choices=[("True", 'True'),("", 'False')], default='True')
    category_id = SelectField('Category Id', validators=[DataRequired()], choices=["1"])