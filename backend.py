from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Allow only specific origins
CORS(app, resources={r"/*": {"origins": ["https://vaseem-ismail.github.io", "http://localhost:5501"]}})

# Configurations
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

mongo = PyMongo(app)
jwt = JWTManager(app)

users_collection = mongo.db.users

# Registration Endpoint
@app.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = {"username": username, "email": email, "password": hashed_password}
    users_collection.insert_one(new_user)

    return jsonify({"message": "User registered successfully"}), 201


# Login Endpoint
@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "Invalid email or password"}), 404

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 400

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({"message": "Login successful", "token": access_token}), 200


# Run App
if __name__ == "__main__":
    app.run(debug=True)
