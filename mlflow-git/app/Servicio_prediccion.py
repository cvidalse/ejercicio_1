import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests import *
from flask_login import LoginManager, UserMixin, login_required
import json
import os

app = Flask('__main__')
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app)


@app.route('/predicciones', methods=['GET'])
@login_required
def proxy_post():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_route = '/controllers/prediccion.json'
    file_option = 'r'
    with open(file_dir + file_route, file_option) as f:
        data = json.load(f)    
    return jsonify(data)

@app.route('/')
def index():
    return "Hello World-This is updated through gitlab pipeline"

class User(UserMixin):
    # proxy for a database of users
    user_database = {"Diufro": ("Diufro", "Diufro_Token")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    try:
        tokenHeader = request.headers['authorization']

        if tokenHeader is None:
            response = jsonify({'message': 'Failed'})
            return response

        if tokenHeader is not None:
            tokenHeader = tokenHeader.replace('Bearer ', '', 1)
            username, password = tokenHeader.split(":")  # naive token
            user_entry = User.get(username)
            if (user_entry is not None):
                user = User(user_entry[0], user_entry[1])
                if (user.password == password):
                    return user
    except:
        flask.abort(401)





@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(host='0.0.0.0', port=8090)

