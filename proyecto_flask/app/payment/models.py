from app.db import db, ma
from app.payment.exceptions import ModelNotFoundError


class RefPaymentMethod(db.Model):
    payment_method_code = db.Column(db.String(20), primary_key=True)
    payment_method_description = db.Column(db.String(100))


class CustomerPaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payment_method_code = db.Column(db.String(20), db.ForeignKey('ref_payment_method.payment_method_code'))
    card_number = db.Column(db.String(50))
    payment_method_details_csv = db.Column(db.String(3))
    payment_method_details_month = db.Column(db.String(3))
    payment_method_details_year = db.Column(db.String(4))


def get_all_payments_by_customer(customer_id):
    payments = db.session.query(CustomerPaymentMethod, RefPaymentMethod) \
        .filter_by(customer_id=customer_id) \
        .filter(CustomerPaymentMethod.payment_method_code == RefPaymentMethod.payment_method_code).all()
    return payments


def get_all_payments_methods():
    payment_methods = RefPaymentMethod.query.all()
    return payment_methods


def create_customer_paymenth(customer_id, payment_method_code, card_number, payment_method_details_csv,
                             payment_method_details_month, payment_method_details_year):
    customer_payment = CustomerPaymentMethod(customer_id=customer_id, payment_method_code=payment_method_code,
                                             card_number=card_number,
                                             payment_method_details_csv=payment_method_details_csv,
                                             payment_method_details_month=payment_method_details_month,
                                             payment_method_details_year=payment_method_details_year)
    db.session.add(customer_payment)
    db.session.commit()
    return customer_payment


def get_payment_by_id(id):
    payment_method = CustomerPaymentMethod.query.filter_by(id=id).first()
    if payment_method:
        return payment_method
    else:
        raise ModelNotFoundError


def update_customer_payment(payment_method_code, card_number, payment_method_details_csv, payment_method_details_month,
                            payment_method_details_year, id):
    customer_payment = CustomerPaymentMethod.query.filter_by(id=id).first()
    customer_payment.payment_method_code = payment_method_code
    customer_payment.card_number = card_number
    customer_payment.payment_method_details_csv = payment_method_details_csv
    customer_payment.payment_method_details_month = payment_method_details_month
    customer_payment.payment_method_details_year = payment_method_details_year

    db.session.add(customer_payment)
    db.session.commit()
    return customer_payment


def delete_customer_payment(id):
    CustomerPaymentMethod.query.filter_by(id=id).delete()
    db.session.commit()
    return True
