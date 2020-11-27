from flask import Flask
from flask_wtf import CSRFProtect

from app.db import db, ma
from conf.config import DevelpmentConfig
from app.products.views import products,tarea3_blueprint
from flask_migrate import Migrate

ACTIVE_ENDPOINTS = [('/tarea3',tarea3_blueprint),('/products', products)]


def create_app(config=DevelpmentConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)    
    csrf.init_app(app)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format="%Y"):
        return value.strftime(format)
    


    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    #Thiss line disable csrf, I have a problem with addStock because it
    csrf.exempt(products)
    
    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()