from flask import Blueprint, Response

tarea3_blueprint = Blueprint('tarea3', __name__, url_prefix='/tarea3')

@tarea3_blueprint.route('/<string:name>')
def index_tarea3(name):
    if name != "pygroup":
        return Response("Felicitaciones! Trabajo exitoso {}".format(name), status=200)
    return Response("ERROR! No se puede usar el nombre pygroup", status=400)