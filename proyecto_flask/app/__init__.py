from flask import Flask
from products import tarea3_blueprint

app = Flask(__name__)

app.register_blueprint(tarea3_blueprint)

if __name__ == "__main__":
    app.run(debug=True)