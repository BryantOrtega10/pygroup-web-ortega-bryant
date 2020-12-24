
from http import HTTPStatus
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.auth.models import User

from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__, url_prefix="/")
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}

@auth.route("/login", methods=["POST"])
def login():
    status_code = HTTPStatus.CREATED
    RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        """ Checks if user does not exists in DB or if the password is 
        invalid. Redirects to login and shows error if this happens."""
        if not user or not check_password_hash(user.password, password):
            RESPONSE_BODY["errors"] = ["Please check your login details and try again."]
            status_code = HTTPStatus.UNAUTHORIZED
            return RESPONSE_BODY, status_code

        login_user(user, remember=remember)
        RESPONSE_BODY["message"] = "Login successfully"
        if(user.rol_id == 1):
            RESPONSE_BODY["data"] = {"redirect" : url_for('products.create_product_form')}
        else:
            RESPONSE_BODY["data"] = {"redirect" : url_for('products.catalog')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code

    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED
        return RESPONSE_BODY, status_code



@auth.route("/signup", methods=["POST"])
def signup():
    status_code = HTTPStatus.CREATED
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        """If user exists shows an error and redirects to signup to try
        with other user.
        """

        if user:
            RESPONSE_BODY["message"] = "User already exist!"
            RESPONSE_BODY["errors"].append("User already exist") 
            status_code = HTTPStatus.BAD_REQUEST
            return RESPONSE_BODY, status_code

        """Creates new user in DB with hashed password for security reasons"""
        new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))

        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=False)
        RESPONSE_BODY["message"] = "Singup successfully"
        RESPONSE_BODY["data"] = {"redirect" : url_for('products.catalog')}
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