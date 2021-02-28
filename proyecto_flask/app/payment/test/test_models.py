import pytest

from app.payment.exceptions import ModelNotFoundError
from app.payment.models import get_payment_by_id, get_all_payments_methods


def test_should_get_payment_method_by_id_when_payment_method_exists_in_db(app, customer_payment):
    with app.app_context():
        result = get_payment_by_id(customer_payment.id)
        assert result.__dict__["card_number"] == customer_payment.card_number


def test_should_raise_error_when_payment_method_does_not_exist_in_db(app):
    with pytest.raises(ModelNotFoundError) as e:
        with app.app_context():
            get_payment_by_id(5)


def test_should_get_all_ref_payments_methods_in_db(app, customer_payment):
    with app.app_context():
        result = get_all_payments_methods()

        assert len(result) > 0

