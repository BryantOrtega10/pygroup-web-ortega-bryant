from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, request, render_template, url_for
from flask_login import current_user, login_required
from app.customer.models import get_customer_by_user_id
from app.payment.forms import CustomerPaymentForm
from app.payment.models import get_all_payments_by_customer, get_all_payments_methods, create_customer_paymenth, \
    get_payment_by_id, update_customer_payment, delete_customer_payment
from app.products.models import get_all_categories

customer_payments = Blueprint("customer-payments", __name__, url_prefix="/customer-payments")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


@customer_payments.route("/", methods=["GET"])
@login_required
def list_of_payments():
    """
        View template of payments methods by customer
        ---
        tags:
          - payments
        parameters:
          - in: path
            name: id
            type: Integer
        responses:
          200:
            description: Template of customer payments
    """

    customer = get_customer_by_user_id(current_user.id)
    payments = get_all_payments_by_customer(customer.id)
    categories = get_all_categories()
    info = {"customer_payments": payments, "categories": categories}
    return render_template("customer_payments.html", info=info)


@customer_payments.route("/add", methods=["GET", "POST"])
@login_required
def add_payment():
    """
        View template of payments methods by customer
        ---
        tags:
          - payments
        parameters:
          - in: formData
            name: payment_method
            type: Integer
            description: foreign key of ref_payment_method
          - in: formData
            name: card_number
            type: Integer
          - in: formData
            name: payment_method_details_csv
            type: Integer
          - in: formData
            name: payment_method_details_month
            type: String
          - in: formData
            name: payment_method_details_year
            type: Integer
        get:
          responses:
            200:
              description: Template of add payment for customer
        post:
          responses:
            200:
              description: Payment added correctly

    """
    customer = get_customer_by_user_id(current_user.id)
    form_payment = CustomerPaymentForm()

    choices_month = [("Ene", "Ene"), ("Feb", "Feb"), ("Mar", "Mar"), ("Abr", "Abr"), ("May", "May"), ("Jun", "Jun"),
                     ("Jul", "Jul"), ("Ago", "Ago"), ("Sep", "Sep"), ("Oct", "Oct"), ("Nov", "Nov"), ("Dic", "Dic")]
    choices_year = []
    now = datetime.now()
    for year in range(now.year, now.year + 5):
        choices_year.append((year, year))

    choices_payment = []
    payment = get_all_payments_methods()
    for pay in payment:
        choices_payment.append((pay.payment_method_code, pay.payment_method_description))

    form_payment.payment_method.choices = choices_payment
    form_payment.payment_method_details_month.choices = choices_month
    form_payment.payment_method_details_year.choices = choices_year

    if request.method == 'POST' and form_payment.validate():
        create_customer_paymenth(customer.id,
                                 form_payment.payment_method.data,
                                 form_payment.card_number.data,
                                 form_payment.payment_method_details_csv.data,
                                 form_payment.payment_method_details_month.data,
                                 form_payment.payment_method_details_year.data,
                                 )
        RESPONSE_BODY["message"] = "Payment added correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('customer-payments.list_of_payments')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code

    return render_template('payment_form_add.html', form=form_payment)


@customer_payments.route("/modify/<int:id>", methods=["GET", "POST"])
@login_required
def modify_payment(id):
    """
        View template of payments methods by id and modify it
        ---
        tags:
          - payments
        parameters:
          - in: path
            name: id
            type: Integer
            description: Id of customer payment method
          - in: formData
            name: payment_method
            type: Integer
            description: foreign key of ref_payment_method
          - in: formData
            name: card_number
            type: Integer
          - in: formData
            name: payment_method_details_csv
            type: Integer
          - in: formData
            name: payment_method_details_month
            type: String
          - in: formData
            name: payment_method_details_year
            type: Integer
        get:
          responses:
            200:
              description: Template of modify payment
        post:
          responses:
            200:
              description: Payment modified correctly
    """
    customer = get_customer_by_user_id(current_user.id)
    payment_select = get_payment_by_id(id)
    form_payment = CustomerPaymentForm()

    choices_month = [("Ene", "Ene"), ("Feb", "Feb"), ("Mar", "Mar"), ("Abr", "Abr"), ("May", "May"), ("Jun", "Jun"),
                     ("Jul", "Jul"), ("Ago", "Ago"), ("Sep", "Sep"), ("Oct", "Oct"), ("Nov", "Nov"), ("Dic", "Dic")]
    choices_year = []
    now = datetime.now()
    for year in range(now.year, now.year + 5):
        choices_year.append((year, year))

    choices_payment = []
    payment = get_all_payments_methods()
    for pay in payment:
        choices_payment.append((pay.payment_method_code, pay.payment_method_description))

    form_payment.payment_method.choices = choices_payment
    form_payment.payment_method_details_month.choices = choices_month
    form_payment.payment_method_details_year.choices = choices_year

    if request.method == 'POST' and form_payment.validate():
        update_customer_payment(form_payment.payment_method.data,
                                form_payment.card_number.data,
                                form_payment.payment_method_details_csv.data,
                                form_payment.payment_method_details_month.data,
                                form_payment.payment_method_details_year.data, id)
        RESPONSE_BODY["message"] = "Payment modified correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('customer-payments.list_of_payments')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        form_payment.payment_method.default = payment_select.payment_method_code
        form_payment.card_number.default = payment_select.card_number
        form_payment.payment_method_details_csv.default = payment_select.payment_method_details_csv
        form_payment.payment_method_details_month.default = payment_select.payment_method_details_month
        form_payment.payment_method_details_year.default = payment_select.payment_method_details_year
        form_payment.process()

    return render_template('payment_form_mod.html', form=form_payment, id=id)

@customer_payments.route("/delete/<int:id>", methods=["GET"])
@login_required
def delete_payment(id):
    """
        Delete customer payment method by id
        ---
        tags:
          - payments
        parameters:
          - in: path
            name: id
            type: Integer
            description: Id of customer payment method
        responses:
          200:
            description: Payment deleted correctly
          400:
              description: Error deleting payment
    """

    if delete_customer_payment(id):
        RESPONSE_BODY["message"] = "Payment deleted correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('customer-payments.list_of_payments')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        RESPONSE_BODY["message"] = "Error deleting payment"
        RESPONSE_BODY["errors"].append("Error deleting payment")
        status_code = HTTPStatus.BAD_REQUEST
        return RESPONSE_BODY, status_code
