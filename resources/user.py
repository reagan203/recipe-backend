# user.py
from models import db, UserModel
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

# Create the user fields
user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "nationality": fields.String,
    "email": fields.String,
    "gender": fields.String,
}

class User(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument("username", required=True, type=str, help="Enter your username")
    user_parser.add_argument("nationality", required=True, type=str, help="Enter your nationality")
    user_parser.add_argument("email", required=True, type=str, help="Enter your email")
    user_parser.add_argument("gender", required=True, type=str, help="Enter your gender")
    user_parser.add_argument("password", required=True, type=str, help="Enter your password")

    @marshal_with(user_fields)
    def get(self, id=None):
        if id:
            user = UserModel.query.filter_by(id=id).first()
            if not user:
                return {"message": "User not found"}, 404
            return user
        else:
            users = UserModel.query.all()
            return users

    def post(self):
        data = User.user_parser.parse_args()

        email = UserModel.query.filter_by(email=data['email']).first()
        if email:
            return {"message": "Email already taken"}, 400

        hashed_password = generate_password_hash(data['password']).decode('utf-8')
        data['password'] = hashed_password
        new_user = UserModel(**data)

        try:
            db.session.add(new_user)
            db.session.commit()

            user_json = new_user.to_json()
            access_token = create_access_token(identity=user_json['id'])
            refresh_token = create_refresh_token(identity=user_json['id'])

            return {
                "message": "Account created successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_json
            }, 201
        except:
            return {"message": "Unable to create user"}, 500

class Login(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('email', required=True, type=str, help="Enter the email")
    user_parser.add_argument('password', required=True, type=str, help="Enter password")

    def post(self):
        data = Login.user_parser.parse_args()

        user = UserModel.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            user_json = user.to_json()
            access_token = create_access_token(identity=user_json['id'])
            refresh_token = create_refresh_token(identity=user_json['id'])

            return {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_json
            }, 200
        return {"message": "Invalid email or password"}, 403
