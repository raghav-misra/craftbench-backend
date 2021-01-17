import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# Init app:
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Default:
@app.route("/", methods=["GET"])
def root(): 
    return "Craftbench REST API @ <a href='https://twitch.tv/AndyDaChicken'>Follow</a>"

# Add routes
import routes_users
import routes_projects