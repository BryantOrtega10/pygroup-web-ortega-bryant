from flask import Flask
from flask_wtf import CSRFProtect

from app.auth.views import auth
from app.auth.models import User,Rol
from app.db import db, ma
from conf.config import DevelpmentConfig
from app.products.views import products,tarea3_blueprint

from flask_migrate import Migrate
from flask_login import LoginManager


ACTIVE_ENDPOINTS = [('/tarea3',tarea3_blueprint),('/products', products),('/', auth)]


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

    #This line disable csrf, I have a problem with addStock because it
    csrf.exempt(auth)
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in
        # the query for the user
        return User.query.get(int(user_id))

    
    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()