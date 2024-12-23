# from flask import Flask, request, jsonify
# from pymongo import MongoClient

# app = Flask(__name__)

# # Replace <username>, <password>, and <cluster-url> with your MongoDB Atlas credentials
# MONGO_URI = "mongodb+srv://mohamedvaseem:mohamedvaseem@anime-galaxy.7lnts.mongodb.net/AnimeDB?retryWrites=true&w=majority"
# client = MongoClient(MONGO_URI)

# # Choose your database and collection
# db = client["testing"]  # Replace "my_database" with your database name
# collection = db["test1"]  # Replace "my_collection" with your collection name

# @app.route("/add", methods=["POST"])
# def add_value():
#     try:
#         # Get JSON data from the request
#         data = request.json

#         # Print or store data (debugging/logging)
#         print(f"Received data: {data}")

#         # Insert data into MongoDB (optional)
#         result = collection.insert_one(data)

#         return jsonify({"message": "Data added successfully", "id": str(result.inserted_id)}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True,port=5001)
    
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient

# App setup
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = '460680e7fe09d19e4063e23c51d3c53757920b054007273cd083703623c1cfea'  # Replace with your actual secret key
jwt = JWTManager(app)

# MongoDB setup
MONGO_URI = "mongodb+srv://mohamedvaseem:mohamedvaseem@anime-galaxy.7lnts.mongodb.net/AnimeDB?retryWrites=true&w=majority"  # Replace with your MongoDB Atlas connection string
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['user_db']
users_collection = db['users']

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password and save the user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users_collection.insert_one({'username': username, 'password': hashed_password}).inserted_id

    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate a JWT token
    token = create_access_token(identity=str(user['_id']))
    return jsonify({'message': 'Login successful', 'token': token}), 200

if __name__ == '__main__':
    app.run(debug=True)
