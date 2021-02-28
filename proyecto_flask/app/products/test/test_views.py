from http import HTTPStatus

import pytest


def test_should_return_404_when_requesting_categories(app, test_client):
    with app.app_context():
        result = test_client.get('products/categories')
        assert result.status_code == HTTPStatus.NOT_FOUND


def test_should_return_200_when_requesting_categories(app, test_client,category):
    with app.app_context():
        result = test_client.get('products/categories')
        assert result.status_code == HTTPStatus.OK