'''
    Es posible devolver la salida de una función vinculada a una determinada URL en forma de HTML.
    Sin embargo, generar contenido HTML a partir del código Python es engorroso, especialmente cuando 
    es necesario colocar datos variables y elementos del lenguaje Python como condicionales o bucles. 
    Aquí es donde se puede aprovechar el motor de plantillas Jinja2, en el que se basa Flask. 
    En lugar de devolver HTML de código rígido desde la función, la función render_template ()
    puede generar un archivo HTML. Flask intentará encontrar el archivo HTML en la carpeta de "templates",
    en la misma carpeta en la que está presente este script.

    El término "sistema de plantillas web" se refiere al diseño de un script HTML en el que los datos variables
    se pueden insertar de forma dinámica. Un sistema de plantillas web consta de un motor de plantillas, 
    algún tipo de fuente de datos y un procesador de plantillas.
    Flask utiliza el motor de plantillas jinja2. Una plantilla web contiene marcadores de posición intercalados 
    de sintaxis HTML para variables y expresiones que son valores reemplazados cuando se representa la plantilla.

    El motor de plantillas jinja2 utiliza los siguientes delimitadores para escapar de HTML.
    {% ...%} para declaraciones
    {{...}} para que las expresiones se impriman en la salida de la plantilla
    {# ... #} para comentarios no incluidos en la salida de la plantilla
    # ... ## para declaraciones de línea
    
    Fuente: https://www.tutorialspoint.com/flask/flask_templates.htm
'''
  
import sys
from http import HTTPStatus

from flask import Blueprint, Response, request, render_template, redirect, \
    url_for
from app.products.forms import CreateCategoryForm, CreateProductForm
from app.products.models import (
    get_all_categories,
    create_new_category,
    get_all_products,
    get_product_by_id,
    create_new_product,
    create_new_stock,
    update_stock
)
products = Blueprint("products", __name__, url_prefix="/products")


EMPTY_SHELVE_TEXT = "Empty shelve!"
PRODUCTS_TITLE = "<h1> Products </h1>"
DUMMY_TEXT = "Dummy method to show how Response works"
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}

@products.route("/dummy-product", methods=["GET", "POST"])
def dummy_product():
    """This method test the request types. If is GET Type it will
    render the text Products in h1 label with code 500.
    If is POST Type it will return Empty shelve! with status code 403
    """
    if request.method == "POST":
        return EMPTY_SHELVE_TEXT, HTTPStatus.FORBIDDEN

    return PRODUCTS_TITLE, HTTPStatus.INTERNAL_SERVER_ERROR


@products.route("/dummy-product-2")
def dummy_product_two():
    """This method shows how Response object could be used to make API
    methods.
    """
    return Response(DUMMY_TEXT, status=HTTPStatus.OK)


@products.route("/categories")
def get_categories():
    """
        Verificar que si get_all_categories es [] 400, message = "No hay nada"
    :return:
    """
    categories = get_all_categories()
    status_code = HTTPStatus.OK

    if categories:
        RESPONSE_BODY["message"] = "OK. Categories List"
        RESPONSE_BODY["data"] = categories
    else:
        RESPONSE_BODY["message"] = "OK. No categories found"
        RESPONSE_BODY["data"] = categories
        status_code = HTTPStatus.NOT_FOUND

    return RESPONSE_BODY, status_code


@products.route("/add-category", methods=["POST"])
def create_category():
    """
    :return:
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
    products_obj = get_all_products()

    RESPONSE_BODY["data"] = products_obj
    RESPONSE_BODY["message"] = "Products list"

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/product/<int:id>")
def get_product(id):
    product = get_product_by_id(id)

    RESPONSE_BODY["data"] = product
    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/product-stock/<int:product_id>")
def get_product_stock(product_id):
    product_stock = get_stock_by_product(product_id)
    RESPONSE_BODY["message"] = "Product stock"
    RESPONSE_BODY["data"] = product_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/need-restock")
def get_products_that_need_restock():
    products_low_stock = get_products_with_low_stock()
    RESPONSE_BODY["message"] = "This products need to be re-stocked"
    RESPONSE_BODY["data"] = products_low_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/register-product-stock/<int:id>", methods=["PUT", "POST"])
def register_product_refund_in_stock(id):

    # TODO Complete this view to update stock for product when a register for
    # this products exists. If not create the new register in DB

    status_code = HTTPStatus.CREATED
    
    if request.method == "PUT":
        data = request.json
        RESPONSE_BODY["data"] = update_stock(id,data["quantity"])   
        status_code = HTTPStatus.OK
        if RESPONSE_BODY["data"] == None :
            RESPONSE_BODY["message"] = "The product stock doesn't exist, use the POST method"   
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
    return render_template('category_success.html')


@products.route('/create-category-form', methods=['GET', 'POST'])
def create_category_form():
    form_category = CreateCategoryForm()
    if request.method == 'POST' and form_category.validate():
        create_new_category(name=form_category.name.data)
        return redirect(url_for('products.category-success'))

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
def create_product_form():
    form_product = CreateProductForm()
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

    return render_template('create_product_form.html', form=form_product)
@products.route('/product-success')
def product_success():
    return render_template('product_success.html')

@products.route('/add-product-old', methods=['GET', 'POST'])
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
    info = {"products": products, "pygroup": "Pygroup 26 de Nov"}
    return render_template("catalog.html", info=info)