from flask import Flask, Response, request
from products import tarea3_blueprint

app = Flask(__name__)
'''
# @app.route('/<string:name>', methods=['POST'])
# def index(name):
#     if len(name) < 5:
#         return Response("Hola {}, tienes un nombre corto".format(name), status=200)
#     return Response("Hola {}, estas usando post".format(name), status=400)

# @app.route('/<string:name>', methods=['GET'])
# def index_get(name):
#     return Response("Hola {}, estas usando get".format(name), status=200)

# @app.route('/menosElaborado/<string:name>', methods=['GET','POST'])
# def index_ambos(name):
#     if request.method == 'POST':
#         return 'Nombre Post: {}'.format(name), 403
#     return '<h1>Nombre Get: {}</h1>'.format(name), 500
'''
app.register_blueprint(tarea3_blueprint)

if __name__ == "__main__":
    app.run(debug=True)