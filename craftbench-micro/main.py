import helpers
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os

# Init app:
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Default:
@app.route("/", methods=["GET"])
@cross_origin()
def root(): return "Craftbench REST API @ <a href='https://twitch.tv/AndyDaChicken'>Follow</a>"

# Return all the projects of one user
@app.route("/get_projects", methods=["POST"])
@cross_origin()
def get_projects():
    return jsonify({
        "success": True,
        "data": helpers.projects_by_username(request.json.get("username"))
    })
    
# Override project data with new project
@app.route("/save_project", methods=["POST"])
@cross_origin()
def save():
    return "TODO"

# Create a new project:
@app.route("/new_project", methods=["POST"])
@cross_origin()
def new_project():
    if helpers.create_project(request.json.get("user_id"), request.json.get("project")):
        return True  # Project was created successfully
    else:
        return False  # Project was not created
    
# Delete a project
@app.route("/delete_project", methods=["POST"])
@cross_origin()
def delete():
    if helpers.delete_project(request.json.get("id")):
        return jsonify({
            "success": True,
        })

    return jsonify({
        "success": False,
        "msg": "Something went wrong deleting that project."
    })

# Add a user
@app.route("/share_projects", methods=["POST"])
@cross_origin()
def share():
    """ Add another user to a project """
    
    return "TODO"

# Signup route!
@app.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    if helpers.check_username_exists(request.json.get("username")):
        return jsonify({
            "success": False,
            "msg": "That username already exists."
        })
    if helpers.create_new_user({
        "username": request.json.get("username"),
        "password_hash": generate_password_hash(request.json.get("password")),
        "name": request.json.get("name"),
        "email": request.json.get("email")
    }):
        return jsonify({
            "success": True,
        })
    else: 
        return jsonify({
            "success": False,
            "msg": "An internal error occurred, retry later."
        }), 500

# Login route!
@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = helpers.user_by_username(username)

    if not user.success: return jsonify({
        "success": False,
        "msg": "Username doesn't exist."
    }), 400

    if not check_password_hash(user.user.password_hash, password): return jsonify({
        "success": False,
        "msg": "Username and password don't match"
    }), 401


    return jsonify({
        "success": True,
        "token": create_access_token(identity=username)
    }), 200