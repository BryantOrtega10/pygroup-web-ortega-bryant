from http import HTTPStatus
from pprint import pprint

from flask import Blueprint, request, render_template, url_for
from flask_login import current_user, login_required
from app.customer.models import get_customer_by_user_id
from app.order.forms import CompleteOrderForm
from app.order.models import get_order_active_by_customer, create_new_order, create_order_item, update_order_item, \
    delete_order_item, get_subtotal_by_customer, create_invoice_by_order_id, get_invoice_by_id, \
    get_order_items_by_order_id, get_subtotal_by_order_id
from app.payment.models import get_all_payments_by_customer
from app.products.models import get_product_by_id, get_all_categories, update_stock, get_stock_by_product

order = Blueprint("order", __name__, url_prefix="/order")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


@order.route("/add-product/<int:product_id>", methods=["GET"])
@login_required
def add_product_to_order_active(product_id):
    """
        Add product and quantity to cart
        ---
        tags:
          - order
        parameters:
          - in: path
            name: product_id
            type: integer
        responses:
          200:
            description: Product added correctly
          400:
            description: The product is out of stock
    """
    stock_product = get_stock_by_product(product_id)
    product = get_product_by_id(product_id)
    customer = get_customer_by_user_id(current_user.id)
    order, order_items = get_order_active_by_customer(customer.id)

    if stock_product["quantity"] > 0:
        if order:
            if order_items:
                product_in_order = search(product["id"], order_items)
                if product_in_order:
                    if product_in_order[0].order_item_status_code == 1:
                        update_order_item(product_in_order[0].id, product_in_order[0].order_item_quantity + 1, product['price'] * (product_in_order[0].order_item_quantity + 1), 1)
                    else:
                        update_order_item(product_in_order[0].id, 1, product['price'], 1)
                else:
                    create_order_item(product_id, order.id, 1, 1, product['price'])
            else:
                create_order_item(product_id, order.id, 1, 1, product['price'])
        else:
            new_order = create_new_order(customer.id)
            create_order_item(product_id, new_order.id, 1, 1, product['price'])

        RESPONSE_BODY["message"] = "Product added correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('order.order_active')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        RESPONSE_BODY["message"] = "The product is out of stock"
        RESPONSE_BODY["errors"].append("The product is out of stock")
        status_code = HTTPStatus.BAD_REQUEST
        return RESPONSE_BODY, status_code



@order.route("/minus-product/<int:product_id>", methods=["GET"])
@login_required
def substract_product_to_order_active(product_id):
    """
        Remove cart products and remove order item if quantity is 0
        ---
        tags:
          - order
        parameters:
          - in: path
            name: product_id
            type: integer
        responses:
          200:
            description: Product subtracted correctly
          404:
            description: Product not found
    """

    customer = get_customer_by_user_id(current_user.id)
    product = get_product_by_id(product_id)
    order, order_items = get_order_active_by_customer(customer.id)
    product_in_order = search(product_id, order_items)
    if len(product_in_order)>0:
        if product_in_order[0].order_item_quantity > 1:
            update_order_item(product_in_order[0].id, product_in_order[0].order_item_quantity - 1, product['price'] * (product_in_order[0].order_item_quantity - 1), 1)
        else:
            delete_order_item(product_in_order[0].id)

        RESPONSE_BODY["message"] = "Product subtracted correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('order.order_active')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        RESPONSE_BODY["message"] = "Product not found"
        RESPONSE_BODY["errors"].append("Product not found")
        status_code = HTTPStatus.NOT_FOUND
        return RESPONSE_BODY, status_code


@order.route("/", methods=["GET"])
@login_required
def order_active():
    """
        Show shopping cart and calculate the subtotal
        ---
        tags:
          - order
        responses:
          200:
            description: Render template of shopping card
    """

    customer = get_customer_by_user_id(current_user.id)
    order, order_items = get_order_active_by_customer(customer.id)

    categories = get_all_categories()

    subtotal = get_subtotal_by_customer(customer.id)
    if subtotal is None:
        subtotal = 0
    tax = subtotal * 0.19
    total = subtotal + tax
    choices_payment = []
    form_order = CompleteOrderForm()
    payments = get_all_payments_by_customer(customer.id)
    for (pay, _) in payments:
        choices_payment.append((pay.id, "XXXX XXXX XXXX " + pay.card_number[-4:]))
    form_order.payment_method.choices = choices_payment
    form_order.address.default = customer.address
    form_order.process()



    info = {"categories":categories, "order": order, "order_items": order_items, "subtotal": subtotal, "tax": tax, "total": total}

    return render_template('order.html', form=form_order, info=info)


@order.route("/remove-product/<int:product_id>", methods=["GET"])
@login_required
def remove_product_from_order_active(product_id):
    """
        Remove order item
        ---
        tags:
          - order
        parameters:
          - in: path
            name: product_id
            type: integer
        responses:
          200:
            description: Product removed correctly
          404:
            description: Product not found
    """
    customer = get_customer_by_user_id(current_user.id)
    order, order_items = get_order_active_by_customer(customer.id)
    product_in_order = search(product_id, order_items)
    delete_order_item(product_in_order[0].id)
    if len(product_in_order)>0:
        RESPONSE_BODY["message"] = "Product removed correctly"
        RESPONSE_BODY["data"] = {'redirect': url_for('order.order_active')}
        status_code = HTTPStatus.OK
        return RESPONSE_BODY, status_code
    else:
        RESPONSE_BODY["message"] = "Product not found"
        RESPONSE_BODY["errors"].append("Product not found")
        status_code = HTTPStatus.NOT_FOUND
        return RESPONSE_BODY, status_code



@order.route("/add_invoice", methods=["POST"])
@login_required
def add_invoice():
    """
        Add an invoice based on an order
        ---
        tags:
          - order
        parameters:
          - in: formData
            name: address
            type: String
          - in: formData
            name: payment_method
            type: Integer
        responses:
          200:
            description: Product removed correctly
          400:
            description: Please fill all fields or There are no items in the order
    """
    form_order = CompleteOrderForm()
    customer = get_customer_by_user_id(current_user.id)
    payments = get_all_payments_by_customer(customer.id)
    choices_payment = []
    for (pay, _) in payments:
        choices_payment.append((pay.id, "XXXX XXXX XXXX " + pay.card_number[-4:]))
    form_order.payment_method.choices = choices_payment

    if form_order.validate():
        customer = get_customer_by_user_id(current_user.id)
        order, order_items = get_order_active_by_customer(customer.id)

        if order_items:

            for (order_item, product, stock) in order_items:
                update_stock(product.id, stock.quantity - order_item.order_item_quantity)

            invoice = create_invoice_by_order_id(order.id, form_order.address.data, form_order.payment_method.data)
            RESPONSE_BODY["message"] = "Invoice created correctly"
            RESPONSE_BODY["data"] = {'redirect': url_for('order.view_invoice', id=invoice.number)}
            status_code = HTTPStatus.OK
            return RESPONSE_BODY, status_code

        RESPONSE_BODY["message"] = "There are no items in the order"
        RESPONSE_BODY["errors"].append("There are no items in the order")
        status_code = HTTPStatus.BAD_REQUEST
        return RESPONSE_BODY, status_code

    RESPONSE_BODY["message"] = "Please fill all fields"
    RESPONSE_BODY["errors"].append("Please fill all fields")
    status_code = HTTPStatus.BAD_REQUEST
    return RESPONSE_BODY, status_code


@order.route("/invoice/<int:id>", methods=["GET"])
@login_required
def view_invoice(id):
    """
        View an invoice by invoice number
        ---
        tags:
          - order
        parameters:
          - in: path
            name: id
            type: Integer
        responses:
          200:
            description: Template of Invoice
    """
    categories = get_all_categories()
    invoice = get_invoice_by_id(id)
    order_items = get_order_items_by_order_id(invoice.order_id)

    subtotal = get_subtotal_by_order_id(invoice.order_id)
    tax = subtotal * 0.19
    total = subtotal + tax

    info = {"categories":categories, "invoice": invoice, "order_items": order_items, "subtotal": subtotal, "tax": tax, "total": total}
    return render_template('invoice.html', info=info)


def search(product_id, order_items):
    return [orderItem for (orderItem, product, stock) in order_items if orderItem.product_id == product_id]
