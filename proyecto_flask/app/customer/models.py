from app.db import db, ma


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100), default="")
    phone_number = db.Column(db.Numeric, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def create_customer(first_name, last_name, email, address, phone_number, user_id):
    customer = Customer(first_name=first_name, last_name=last_name, email=email, address=address,
                        phone_number=phone_number, user_id=user_id)
    db.session.add(customer)
    db.session.commit()
    return customer


def get_customer_by_email(email):
    customer = Customer.query.filter_by(email=email).first()
    return customer


def get_customer_by_user_id(user_id):
    customer = Customer.query.filter_by(user_id=user_id).first()
    return customer


def update_customer(first_name, last_name, email, address, phone_number, id):
    customer = Customer.query.filter_by(id=id).first()
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.address = address
    customer.phone_number = phone_number
    db.session.add(customer)
    db.session.commit()
    return customer
