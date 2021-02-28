import pytest

from app.customer.models import get_customer_by_user_id,get_customer_by_email


def test_should_get_customer_by_user_id_when_user_exists_in_db(app, customer):
    with app.app_context():
        result = get_customer_by_user_id(customer.user_id)
        assert result.__dict__["email"] == customer.email


def test_should_get_none_when_customer_doesnt_exists_in_db(app):
    with app.app_context():
        result = get_customer_by_user_id(1)
        assert result is None


def test_should_get_customer_by_email_when_user_exists_in_db(app, customer):
    with app.app_context():
        result = get_customer_by_email(customer.email)
        assert result.__dict__["email"] == customer.email


def test_should_get_none_when_email_doesnt_exists_in_db(app):
    with app.app_context():
        result = get_customer_by_email("test2@test.com")
        assert result is None

