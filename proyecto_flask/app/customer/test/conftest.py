import pytest
import sqlalchemy
from werkzeug.security import generate_password_hash

from app import create_app, User
from app.customer.models import Customer
from app.db import create_all, db, drop_all
from app.order.models import OrderItem, Order, RefInvoiceStatusCode, RefOrderStatusCode, RefOrderItemStatusCode
from app.products.models import Product
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

def create_user():
    user = User(username="test", password=generate_password_hash("test", method="sha256"))
    db.session.add(user)
    db.session.commit()
    return user


def create_test_customer():
    user = create_user()
    customer = Customer(first_name="Test_client", last_name="Test_client last name", email="test@test.com",
                        address="",
                        phone_number="0000000", user_id=user.id)

    db.session.add(customer)
    db.session.commit()
    return customer



@pytest.fixture
def customer(app):
    with app.app_context():
        return create_test_customer()


@pytest.fixture
def user(app):
    with app.app_context():
        return create_user()

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
def form_new_payment_ok(app):
    return {'name': 'Categoria pruebas 123'}
