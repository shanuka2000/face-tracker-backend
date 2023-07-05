# imports
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# app configs
app = Flask(__name__)
CORS(app)

# DB Configs
usename = "shanukase"
password = "8Ejay0sufP6hTbOM"
cluster_name = "cluster0"
database_name = "face-tracker"
collection_name = "sessionData"

# Create a MongoDB client
connection_string = f"mongodb+srv://{usename}:{password}@{cluster_name}.yj3jrtg.mongodb.net/{database_name}?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client[database_name]
collection = db[collection_name]

# Get one item
@app.route("/session/one", methods=["GET"])
def get_one_session():
    try:
        session_id = request.args.get("sessionId")
        query = {"sessionId": session_id}
        data = collection.find_one(query)
        data["_id"] = str(data["_id"])

        return jsonify(data)
    except Exception as e:
        return f"Error retrieving data: {str(e)}"

# Get all data
@app.route('/session/all', methods=["GET"])
def get_sessions():
    try:
        data = list(collection.find())
        json_data = []

        for document in data:
            document["_id"] = str(document["_id"])
            json_data.append(document)

        return jsonify(json_data)
    except Exception as e:
        return f"Error retrieving data: {str(e)}"

# Health Check endpoint
@app.route('/', methods=["GET"])
def check_health():
    try:
        # Test the connection by accessing a collection
        return f"Application works successfully and connected to MongoDB Atlas", 200
    except Exception as e:
        return f"Connection failed to MongoDB Atlas", 500

# 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)