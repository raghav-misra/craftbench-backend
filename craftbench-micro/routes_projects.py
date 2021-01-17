import helpers
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from main import app

# Return all the projects of one user
@app.route("/projects/get", methods=["POST"])
def projects_get():
    # Send what they own and query again for what they are a member of
    return jsonify({
        "success": True,
        "data": helpers.projects_by_username(request.json.get("username"))
    })
    
# Override project data with new project
@app.route("/projects/save", methods=["POST"])
def projects_save():
    if helpers.update_project(request.json.get("project_id"), request.json.get("data")):
        return {"message": "Successfully updated"}
    return {"message": "Could not update" }

# Create a new project:
@app.route("/projects/create", methods=["POST"])
def projects_create():
    if helpers.create_project(request.json.get("data")):
        return {"success": True}  # Project was created successfully
    else:
        return {"success": False}  # Project was not created
    
# Delete a project
@app.route("/projects/delete", methods=["POST"])
def projects_delete():
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
def projects_add_user():
    """ Add another user to a project """

    project_id = request.json.get("project_id")
    new_id = request.json.get("id")
    if helpers.add_user(new_id, project_id):
        return { "message": "Successsfully added user to this project" }

    return { "message": "Could not add user to this project" }