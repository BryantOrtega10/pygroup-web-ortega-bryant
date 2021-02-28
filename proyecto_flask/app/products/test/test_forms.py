from http import HTTPStatus
from flask import url_for

import pytest


def test_should_return_succes_category_when_submit_form(app, test_client, form_new_category_ok):
    with app.app_context():
        form_url = "/products/create-category-form"
  
        
        result = test_client.post(form_url, data=form_new_category_ok, follow_redirects=True)
        assert b'Category created successfully' in result.data


def test_should_return_fail_category_when_submit_form(app, test_client, form_new_category_fail):
    with app.app_context():
        form_url = "/products/create-category-form"
  
        
        result = test_client.post(form_url, data=form_new_category_fail, follow_redirects=True)
        assert b'Category created successfully' not in result.data


