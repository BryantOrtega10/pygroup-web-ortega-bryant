from flask import Flask, redirect, url_for, jsonify
from flask_wtf import CSRFProtect
from app.auth.views import auth
from app.auth.models import User, Rol
from app.db import db, ma
from app.order.views import order
from app.payment.views import customer_payments
from conf.config import DevelpmentConfig
from app.products.views import products, tarea3_blueprint
from app.customer.views import customers
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

ACTIVE_ENDPOINTS = [('/tarea3', tarea3_blueprint), ('/products', products), ('/', auth), ('/customers', customers),
                    ('/customer-payments', customer_payments), ('/order', order)]

SWAGGER_URL = '/swagger'
API_URL = '/spec'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Pygroup Shop"
    }
)


def create_app(config=DevelpmentConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    app.config.from_object(config)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format="%Y"):
        return value.strftime(format)

    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    # This line disable csrf, I have a problem with addStock because it
    csrf.exempt(auth)
    csrf.exempt(products)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in
        # the query for the user
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return redirect(url_for("products.catalog"))

    @app.route("/spec")
    def spect():
        swag = swagger(app)
        swag['info']['version'] = "1.0.0"
        swag['info']['title'] = "Pygroup Shop"
        swag['info']['description'] = "My Shoe Shop"
        return jsonify(swag)

    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()
