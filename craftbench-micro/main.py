import helpers
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os

# Init app:
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Default:
@app.route("/", methods=["GET"])
@cross_origin()
def root(): 
    return "Craftbench REST API @ <a href='https://twitch.tv/AndyDaChicken'>Follow</a>"

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
    if helpers.update_project(request.json.get("project_id"), request.json.get("data")):
        return {"message": "Successfully updated"}
    return {"message": "Could not update" }

# Create a new project:
@app.route("/new_project", methods=["POST"])
@cross_origin()
def new_project():
    if helpers.create_project(request.json.get("project")):
        return {"success": True}  # Project was created successfully
    else:
        return {"success": False}  # Project was not created
    
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
@app.route("/projects/add_user", methods=["POST"])
@cross_origin()
def projects_share():
    """ Add another user to a project """

    
    helpers.add_user(request.json.get("id"), request.json.get("project_id"))

    return "TODO"

# Signup route!
@app.route("/users/create", methods=["POST"])
@cross_origin()
def users_create():
    if helpers.check_username_exists(request.json.get("username")):
        return jsonify({
            "success": False,
            "msg": "That username already exists."
        }), 400
    if helpers.create_new_user({
        "username": request.json.get("username"),
        "password_hash": generate_password_hash(request.json.get("password")),
        "name": request.json.get("name"),
        "email": request.json.get("email")
    }):
        return jsonify({
            "success": True,
        }), 201
    else: 
        return jsonify({
            "success": False,
            "msg": "An internal error occurred, retry later."
        }), 500

# Login route!
@app.route("/users/login", methods=["POST"])
@cross_origin()
def users_login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = helpers.user_by_username(username)

    if not user["success"]: return jsonify({
        "success": False,
        "msg": "Username doesn't exist."
    }), 400

    if not check_password_hash(user["user"]["data"]["password_hash"], password): return jsonify({
        "success": False,
        "msg": "Username and password don't match"
    }), 401


    return jsonify({
        "success": True,
        "token": create_access_token(identity=user["user"]["ref"].id())
    }), 201

@app.route("/users/get", methods=["GET"])
@jwt_required
def users_get():
    current_user = get_jwt_identity()
    return jsonify({}), 201
