# imports
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import time

# app configs
app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

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


def generate_images(num_samples, sampled_labels):
    latent_dim = 100

    # Load the generator model
    generator = load_model('generator_model.h5')

    # Generate noise vectors
    noise = np.random.normal(0, 1, (num_samples, latent_dim))

    # Use the generator to create new images
    generated_images = generator.predict([noise, sampled_labels])

    # Rescale images from range -1 to 1 to range 0 to 1
    generated_images = 0.5 * generated_images + 0.5

    # Save the generated images as files and get their paths
    image_paths = []
    timestamp = int(time.time())  # Get a timestamp for uniqueness
    for i, img in enumerate(generated_images):
        # Create a unique filename for each image
        filename = f"image_{timestamp}_{i+1}.png"

        # Save the image as a file
        save_path = os.path.join("static/images_generated", filename)
        plt.imsave(save_path, img)

        # Append the image path to the list
        image_paths.append(save_path)

    return image_paths

# Generate image endpoint


@app.route('/features/generate', methods=["POST"])
def generate_image():
    try:
        # return json_data
        sampled_labels = np.array([list(request.get_json())])
        generated_image_paths = generate_images(
            num_samples=1, sampled_labels=sampled_labels)

        # Return the file paths as a JSON response
        response_data = {
            "image_paths": generated_image_paths
        }

        return json.dumps(response_data)
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Save session data endpoint


@app.route('/session/save', methods=["POST"])
def save_session():
    try:
        data = request.get_json()
        collection.insert_one(data)
        return "Data saved Successfully"
    except Exception as e:
        return f"Error saving data: {str(e)}"

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
