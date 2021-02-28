from http import HTTPStatus

from flask import Blueprint, request, render_template, url_for
from flask_login import current_user, login_required

from app.auth.models import get_user_by_username, update_user, update_password
from app.customer.forms import ProfileForm
from app.customer.models import get_customer_by_user_id, update_customer

customers = Blueprint("customers", __name__, url_prefix="/customers")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


@customers.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
        Modify and view data of customer
        ---
        tags:
          - customer
        get:
          description: Render template of customer profile
          responses:
            200:
              description: Render template of customer profile
        post:
          description: Modify data of customer profile
          responses:
            200:
              description: Change applied correctly
            400:
              description: The passwords not match or User already exist
          parameters:
            - in: formData
              name: first_name
              type: String
            - in: formData
              name: last_name
              type: String
            - in: formData
              name: email
              type: String
            - in: formData
              name: phone_number
              type: Number
            - in: formData
              name: username
              type: String
    """
    customer = get_customer_by_user_id(current_user.id)
    form_profile = ProfileForm()
    if request.method == 'POST' and form_profile.validate():
        if form_profile.username.data != current_user.username:
            user = get_user_by_username(form_profile.username.data)
            if user:
                RESPONSE_BODY["message"] = "User already exist!"
                RESPONSE_BODY["errors"].append("Username already exist")
                status_code = HTTPStatus.BAD_REQUEST
                return RESPONSE_BODY, status_code
            new_user = update_user(current_user.id, form_profile.username.data)
            current_user.username = new_user.username

        if form_profile.password.data != "":
            if form_profile.r_password.data == form_profile.password.data:
                update_password(current_user.id, form_profile.password.data)
            else:
                RESPONSE_BODY["message"] = "The passwords not match!"
                RESPONSE_BODY["errors"].append("The passwords not match°")
                status_code = HTTPStatus.BAD_REQUEST
                return RESPONSE_BODY, status_code

        update_customer(form_profile.first_name.data,
                        form_profile.last_name.data,
                        form_profile.email.data,
                        form_profile.address.data,
                        form_profile.phone_number.data,
                        customer.id)

        RESPONSE_BODY["message"] = "Change applied correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('products.catalog')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        form_profile.first_name.default = customer.first_name
        form_profile.last_name.default = customer.last_name
        form_profile.email.default = customer.email
        form_profile.address.default = customer.address
        form_profile.phone_number.default = customer.phone_number
        form_profile.username.default = current_user.username
        form_profile.process()

    return render_template('customer_profile.html', form=form_profile)
