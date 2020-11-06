from flask import Blueprint, Response

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