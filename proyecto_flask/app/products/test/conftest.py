import pytest
import sqlalchemy

from app import create_app
from app.db import create_all, db, drop_all
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


@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(name="fake-product", price=1, description="foo",
                          refundable=True)
        db.session.add(product)
        db.session.commit()
        return product


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
def category(app):
    with app.app_context():
        category = Category(name="fake-category")
        db.session.add(category)
        db.session.commit()
        return category