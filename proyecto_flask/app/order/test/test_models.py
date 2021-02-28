import pytest

from app.order.models import get_subtotal_by_order_id,get_order_active_by_customer


def test_should_get_subtotal_by_order_id_when_order_exists_in_db(app, order_item):
    with app.app_context():
        result = get_subtotal_by_order_id(order_item.order_id)
        assert result == order_item.order_item_price


def test_should_get_none_by_order_id_when_order_doesnt_exists_in_db(app):
    with app.app_context():
        result = get_subtotal_by_order_id("ORD_123_123")
        assert result is None


def test_should_get_order_by_customer_when_customer_exists_in_db(app, order):
    with app.app_context():
        result = get_order_active_by_customer(order.customer_id)
        assert result is not None


def test_should_get_none_by_customer_when_customer_doesnt_exists_in_db(app):
    with app.app_context():
        result = get_order_active_by_customer(5)
        assert result is not None
