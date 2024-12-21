from flask import Flask, request, jsonify
import json
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Allow only specific origins
CORS(app, resources={r"/*": {"origins": ["https://vaseem-ismail.github.io", "http://localhost:5500"]}})

# Configurations
app.config["MONGO_URI"] = os.getenv("MONGO_URI")  # Ensure MONGO_URI is set correctly in .env
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Ensure JWT_SECRET_KEY is set in .env

mongo = PyMongo(app)
jwt = JWTManager(app)

# Connect to the specific database and collection
anime_db = mongo.cx["AnimeDB"]  # Explicitly use AnimeDB
users_collection = anime_db["users"]

# Utility function for JSON serialization of ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


app.json_encoder = JSONEncoder

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
    app.run(debug=True, host="0.0.0.0", port=5000)
