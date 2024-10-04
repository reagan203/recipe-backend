# app.py
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db,UserModel
from resources.user import Login,User
from resources.recipe import Recipe
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configuring app using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


# Initialize the database
db.init_app(app)

migrations = Migrate(app,db)

# Get the current user from jwt 
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none().to_json()

api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Recipe, '/recipes', '/recipes/<int:id>')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000,debug=False)
