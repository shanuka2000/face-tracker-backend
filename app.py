# imports
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# app configs
app = Flask(__name__)
CORS(app)

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