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


def create_test_customer():
    user = User(username="test", password=generate_password_hash("test", method="sha256"))
    customer = Customer(first_name="Test_client", last_name="Test_client last name", email="test@test.com",
                        address="",
                        phone_number="0000000", user_id=user.id)
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()
    return customer


def create_test_order():
    customer = create_test_customer()
    ref1 = RefOrderStatusCode(order_status_code=1, order_status_description="ACTIVE")
    ref2 = RefOrderStatusCode(order_status_code=2, order_status_description="CANCEL")
    ref3 = RefOrderStatusCode(order_status_code=3, order_status_description="IN_PAY")
    db.session.add(ref1)
    db.session.add(ref2)
    db.session.add(ref3)
    order = Order(id="ORD_1_1", customer_id=customer.id, order_status_code=ref1.order_status_code)
    db.session.add(order)
    db.session.commit()
    return order


def create_test_order_item():
    order = create_test_order()
    ref1 = RefOrderItemStatusCode(order_item_status_code=1,order_item_status_description="ACTIVE")
    ref2 = RefOrderItemStatusCode(order_item_status_code=2,order_item_status_description="REMOVED")
    db.session.add(ref1)
    db.session.add(ref2)
    product = Product(name="fake-product", price=1, description="foo",
                      refundable=True)
    db.session.add(product)
    order_item = OrderItem(id="ORD_ITEM_1_1", product_id=product.id, order_id=order.id,
                           order_item_status_code=ref1.order_item_status_code, order_item_quantity=1,
                           order_item_price=product.price)
    db.session.add(order_item)
    db.session.commit()
    return order_item


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
def order(app):
    with app.app_context():
        order = create_test_order()
        return order

@pytest.fixture
def order_item(app):
    with app.app_context():
        order_item = create_test_order_item()
        return order_item


@pytest.fixture
def form_new_payment_ok(app):
    return {'name': 'Categoria pruebas 123'}
