import sys
from http import HTTPStatus

from flask import Blueprint, Response, request, render_template, redirect, url_for

from app.customer.models import get_customer_by_user_id
from app.order.models import get_order_active_by_customer
from app.products.forms import CreateCategoryForm, CreateProductForm
from app.products.models import (
    get_all_categories,
    create_new_category,
    get_all_products,
    get_product_by_id,
    create_new_product,
    create_new_stock,
    update_stock, get_products_with_low_stock, get_stock_by_product, get_all_products_by_cat, get_category_by_id
)
from flask_login import login_required, current_user

products = Blueprint("products", __name__, url_prefix="/products")


EMPTY_SHELVE_TEXT = "Empty shelve!"
PRODUCTS_TITLE = "<h1> Products </h1>"
DUMMY_TEXT = "Dummy method to show how Response works"
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}

@products.route("/categories")
def get_categories():
    """
        Get all categories 
        ---
        tags:
          - products
        responses:
          200:
            description: Categories List
          400:
              description: No categories found
    """
    categories = get_all_categories()
    status_code = HTTPStatus.OK

    if categories:
        RESPONSE_BODY["message"] = "Categories List"
        RESPONSE_BODY["data"] = categories
    else:
        RESPONSE_BODY["message"] = "No categories found"
        RESPONSE_BODY["data"] = categories
        status_code = HTTPStatus.NOT_FOUND

    return RESPONSE_BODY, status_code


@products.route("/add-category", methods=["POST"])
def create_category():
    """
        Create category with name
        ---
        tags:
          - products
        post:
            parameters:
              -in: formData
              name: name
              description: name of category
              schema:
                type: array
                items:
                  name: string
            responses:
              201:
                description: Category created
              405:
                  description: No categories found
    """

    RESPONSE_BODY["message"] = "Method not allowed"
    status_code = HTTPStatus.METHOD_NOT_ALLOWED
    if request.method == "POST":
        data = request.json
        category = create_new_category(data["name"])
        RESPONSE_BODY["message"] = "OK. Category created!"
        RESPONSE_BODY["data"] = category
        status_code = HTTPStatus.CREATED

    return RESPONSE_BODY, status_code


@products.route("/")
def get_products():
    """
        Get all products
        ---
        tags:
          - products
        responses:
          200:
            description: Products List
    """

    products_obj = get_all_products()

    RESPONSE_BODY["data"] = products_obj
    RESPONSE_BODY["message"] = "Products list"

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/product-stock/<int:product_id>")
def get_product_stock(product_id):
    """
        Get stock by product id
        ---
        tags:
          - products
        parameters:
          - in: path
            name: product_id
            type: Integer
        responses:
          200:
            description: Product stock
            data: array of products
    """
    product_stock = get_stock_by_product(product_id)
    RESPONSE_BODY["message"] = "Product stock"
    RESPONSE_BODY["data"] = product_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/need-restock")
def get_products_that_need_restock():
    """
        get products when stock is less than 5
        ---
        tags:
          - products
        parameters:
          - in: path
            name: product_id
            type: Integer
        responses:
          200:
            description: This products need to be re-stocked
            data: array of products of low stock
    """
    products_low_stock = get_products_with_low_stock()
    RESPONSE_BODY["message"] = "This products need to be re-stocked"
    RESPONSE_BODY["data"] = products_low_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/register-product-stock/<int:id>", methods=["PUT", "POST"])
def register_product_refund_in_stock(id):

    """
        get products when stock is less than 5
        ---
        tags:
          - products
        put:
            parameters:
              - in: path
                name: id
                type: Integer
              - in: path
                name: quantity
                type: Integer
            responses:
              200:
                description: The product stock doesn't exist, use the POST method
              405:
                description: Method not Allowed
        post:
            parameters:
              - in: path
                name: id
                type: Integer
                description: product_id
              - in: path
                name: quantity
                type: Integer
            responses:
              200:
                description: Stock for this product were updated successfully
              405:
                description: Method not Allowed
    """

    status_code = HTTPStatus.CREATED
    
    if request.method == "PUT":
        data = request.json
        RESPONSE_BODY["data"] = update_stock(id,data["quantity"])   
        status_code = HTTPStatus.OK
        if RESPONSE_BODY["data"] is None:
            RESPONSE_BODY["message"] = "The product stock doesn't exist, use the POST method"
            status_code = HTTPStatus.METHOD_NOT_ALLOWED
        else:
            RESPONSE_BODY["message"] = \
                "Stock for this product were updated successfully!"
        
    elif request.method == "POST":
        data = request.json
        create_new_stock(id, data["quantity"])
        RESPONSE_BODY["message"] = "Stock for this product were created successfully!"

        pass
    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED

    return RESPONSE_BODY, status_code


@products.route('/category-success')
def category_success():
    """
        Render category success
        ---
        tags:
          - products
        responses:
          200:
            description: render template category success
    """

    return render_template('category_success.html')


@products.route('/create-category-form', methods=['GET', 'POST'])
def create_category_form():
    form_category = CreateCategoryForm()
    if request.method == 'POST' and form_category.validate():
        create_new_category(name=form_category.name.data)
        return redirect(url_for('products.category_success'))

    return render_template('create_category_form.html', form=form_category)

@products.route('/add-category-old', methods=['GET', 'POST'])
def create_category_old():
    if request.method=='POST':
        category = create_new_category(request.form["name"])
        RESPONSE_BODY["message"] = "Se agrego la categoria {} con exito".format(request.form["name"])
        RESPONSE_BODY["data"] = category
        status_code = HTTPStatus.CREATED
        return RESPONSE_BODY, status_code
    return render_template("form_category_old.html")

tarea3_blueprint = Blueprint('tarea3', __name__, url_prefix='/tarea3')
@tarea3_blueprint.route('/<string:name>')
def index_tarea3(name):
    """
        Description: This method show a message for different values, if value is pygroup shows an error with code 400
        parameters: name = String with a name 
        return: Response    400 in case of value of parameter is "pygroup"
                            200 in another case
    """

    if name != "pygroup":
        return Response("Felicitaciones! Trabajo exitoso {}".format(name), status=200)
    return Response("ERROR! No se puede usar el nombre pygroup", status=400)

@products.route('/create-product-form', methods=['GET', 'POST'])
@login_required
def create_product_form():
    form_product = CreateProductForm()
    categories = get_all_categories()
    print(categories)
    choices = []
    for category in categories:
        choices.append((category["id"], category["name"]))

    form_product.category_id.choices = choices


    if request.method == 'POST' and form_product.validate():
        name = form_product.name.data
        image = form_product.image.data
        price = form_product.price.data
        weight = form_product.weight.data
        description = form_product.description.data
        refundable = bool(form_product.refundable.data)
        category_id = form_product.category_id.data

        create_new_product( name=name,
                            image=image,
                            price=price,
                            weight=weight,
                            description=description,
                            refundable=refundable,
                            category_id=category_id)
        return redirect(url_for('products.product_success'))
    form_product.process()

    return render_template('create_product_form.html', form=form_product)
@products.route('/product-success')
def product_success():
    return render_template('product_success.html')

@products.route('/add-product-old', methods=['GET', 'POST'])
@login_required
def create_product_old():
    if request.method=='POST':
        name = request.form["name"]
        image = request.form["image"]
        price = request.form["price"]
        weight = request.form["weight"]
        description = request.form["description"]
        refundable = bool(request.form["refundable"])
        category_id = request.form["category_id"]

        create_new_product( name=name,
                            image=image,
                            price=price,
                            weight=weight,
                            description=description,
                            refundable=refundable,
                            category_id=category_id)
        return redirect(url_for('products.product_success'))
    return render_template("form_product_old.html")


@products.route("/catalog", methods=['GET'])
def catalog():
    products = get_all_products()
    categories = get_all_categories()

    info = {"products": products, "pygroup": "Pygroup 26 de Nov", "categories": categories}

    return render_template("catalog.html", info=info)


@products.route("/product/<int:id>")
def get_product(id):
    product = get_product_by_id(id)
    stock = get_stock_by_product(id)
    categories = get_all_categories()
    if current_user.is_authenticated:
        customer = get_customer_by_user_id(current_user.id)
        order, order_items = get_order_active_by_customer(customer.id)
    else:
        order, order_items = None, None

    addition_method = {"type": "button"}
    if order:
        if order_items:
            product_in_order = search(product["id"], order_items)
            if product_in_order:
                addition_method = {"type": "plus_minus", "quantity": product_in_order[0].order_item_quantity, "code": product_in_order[0].order_item_status_code, }

    info = {"product": product, "categories": categories,
            "addition_method": addition_method, "stock": stock}
    return render_template("product.html", info=info)


@products.route("/product-category/<int:id>")
def get_products_by_cat(id):

    products = get_all_products_by_cat(id)
    categories = get_all_categories()
    category = get_category_by_id(id)
    info = {"products": products, "categories": categories, "category": category}

    return render_template("products_by_cat.html", info=info)

def search(product_id, order_items):
    return [orderItem for (orderItem, product, stock) in order_items if orderItem.product_id == product_id]
