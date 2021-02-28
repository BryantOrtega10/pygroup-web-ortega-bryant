import pytest
import sqlalchemy
from werkzeug.security import generate_password_hash

from app import create_app, User
from app.customer.models import Customer
from app.db import create_all, db, drop_all
from app.payment.models import CustomerPaymentMethod, RefPaymentMethod
from app.products.models import Product, Category
from conf.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(config=TestingConfig)
    with app.app_context():
        create_all()
        app.teardown_bkp = app.teardown_appcontext_funcs
        app.teardown_appcontext_funcs = []
        yield app  # provide the fixture value
        drop_all()

    return app

def create_test_customer():
    user = User(username="test", password=generate_password_hash("test", method="sha256"))
    customer = Customer(first_name="Test_client", last_name="Test_client last name", email="test@test.com",
                        address="",
                        phone_number="0000000", user_id=user.id)
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()
    return customer


@pytest.fixture
def customer(app):
    with app.app_context():
        return create_test_customer()


@pytest.fixture
def test_client(app):
    # Flask provides a way to test your application by exposing the Werkzeug
    # test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture
def customer_payment(app):
    with app.app_context():
        customer = create_test_customer()
        payment_method_code = RefPaymentMethod(payment_method_code=1, payment_method_description="Credit")
        customer_payment = CustomerPaymentMethod(customer_id=customer.id,
                                                 payment_method_code=payment_method_code.payment_method_code,
                                                 card_number="1111111111111111", payment_method_details_csv="111",
                                                 payment_method_details_month="06", payment_method_details_year="2025")
        db.session.add(payment_method_code)
        db.session.add(customer_payment)
        db.session.commit()
        return customer_payment


@pytest.fixture
def form_new_payment_ok(app):
    return {'name': 'Categoria pruebas 123'}
