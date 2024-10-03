from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Store hashed passwords
    nationality = db.Column(db.String(139), nullable=False)  # Fixed the case for Column and String
    email = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'nationality': self.nationality,
            'email': self.email,
            'gender': self.gender
        }


class RecipeModel(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # List of ingredients
    instructions = db.Column(db.Text, nullable=False)  # Cooking instructions
    cooking_time = db.Column(db.Integer, nullable=False)  # Time in minutes
