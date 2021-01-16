from helpers import projects_by_username, create_project, check_username_exists
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Init app:
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# If the username exists, return True
@app.route("/username_exists", methods=["POST"])
@cross_origin()
def username_exists():
    return False

# Return all the projects of one user
@app.route("/get_projects", methods=["POST"])
@cross_origin()
def get_projects():
    return jsonify(projects_by_username(request.json.get("username")))
    

@app.route("/save_project", methods=["POST"])
@cross_origin()
def save():
    """ Override project data with new project """
    return "TODO"

@app.route("/new_project", methods=["POST"])
@cross_origin()
def new_project():
    create_project(request.json)
    return "Lets go it worked"



@app.route("/delete_project", methods=["POST"])
@cross_origin()
def delete():
    """ Delete a project """
    return "TODO"

@app.route("/share_projects", methods=["POST"])
@cross_origin()
def share():
    """ Return all the projects of one user """
    return "TODO"

@app.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    username = request.json.get("username")
    password = request.json.get("signup")
    password_hash = generate_password_hash(password)
    username_exists = check_username_exists(username)
    print("urmom", username_exists)
    return jsonify({
        "success": True,
        "username_exists": False,
        "message": str(username_exists)
    })