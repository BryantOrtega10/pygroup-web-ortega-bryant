from http import HTTPStatus
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.customer.models import get_customer_by_email, create_customer
from app.db import db
from app.auth.models import User, get_user_by_username, create_user, get_user

from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__, url_prefix="/")
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


@auth.route("/login", methods=["POST"])
def login():
    status_code = HTTPStatus.CREATED
    RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = get_user(username, password)

        """ Checks if user does not exists in DB or if the password is 
        invalid. Redirects to login and shows error if this happens."""
        if not user:
            RESPONSE_BODY["errors"] = ["Please check your login details and try again."]
            status_code = HTTPStatus.UNAUTHORIZED
            return RESPONSE_BODY, status_code

        login_user(user, remember=remember)
        RESPONSE_BODY["message"] = "Login successfully"
        if (user.rol_id == 1):
            RESPONSE_BODY["data"] = {"redirect": url_for('products.create_product_form')}
        else:
            RESPONSE_BODY["data"] = {"redirect": url_for('products.catalog')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code

    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED
        return RESPONSE_BODY, status_code


@auth.route("/signup", methods=["POST"])
def signup():
    status_code = HTTPStatus.CREATED
    RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")
        username = request.form.get("username")
        password = request.form.get("password")
        r_password = request.form.get("r_password")

        if password != r_password:
            RESPONSE_BODY["message"] = "The passwords not match!"
            RESPONSE_BODY["errors"].append("The passwords not match")
            status_code = HTTPStatus.BAD_REQUEST
            return RESPONSE_BODY, status_code

        user = get_user_by_username(username)

        """If user exists shows an error and redirects to signup to try
        with other user.
        """
        if user:
            RESPONSE_BODY["message"] = "User already exist!"
            RESPONSE_BODY["errors"].append("Username already exist")
            status_code = HTTPStatus.BAD_REQUEST
            return RESPONSE_BODY, status_code

        customer = get_customer_by_email(email)
        if customer:
            RESPONSE_BODY["message"] = "Email already exist!"
            RESPONSE_BODY["errors"].append("Email already exist")
            status_code = HTTPStatus.BAD_REQUEST
            return RESPONSE_BODY, status_code

        """Creates new user in DB with hashed password for security reasons"""

        new_user = create_user(username, password)
        new_cusmtomer = create_customer(first_name, last_name, email, address, phone_number, new_user.id)

        login_user(new_user, remember=False)
        RESPONSE_BODY["message"] = "Singup successfully"
        RESPONSE_BODY["data"] = {"redirect": url_for('products.catalog')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED
        return RESPONSE_BODY, status_code


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("products.catalog"))
