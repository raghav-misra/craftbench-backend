import helpers
from flask import request, jsonify

from main import app

# Return all the projects of one user
@app.route("/projects/get", methods=["POST"])
def projects_get():
    # token_response = helpers.validate_jwt(request)
    # if not token_response["success"]:
    #     return jsonify(token_response), 401

    # Send what they own and query again for what they are a member of
    return jsonify({
        "success": True,
        "projects": helpers.projects_by_username(request.json.get("username"))
    })

# Override project data with new project
@app.route("/projects/save", methods=["POST"])
def projects_save():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    if helpers.update_project(request.json.get("project_id"), request.json.get("data")):
        return { "msg": "Successfully updated" }
    return {"msg": "Could not update" }

# Create a new project:
@app.route("/projects/create", methods=["POST"])
def projects_create():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401

    project_query = helpers.create_project(request, token_response["id"])
    if project_query["success"]:
        return jsonify({ 
            "success": True,
            "data": {
                "id": project_query["data"]["ref"].id()
            }
            # "project_id": 
        }), 201  # Project was created successfully
    else:
        return jsonify({ 
            "success": False 
        }), 500  # Project was not created

@app.route("/projects/delete", methods=["POST"])
def projects_delete():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    if helpers.delete_project(request.json.get("project_id")):
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
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    """ Add another user to a project """
    project_id = request.json.get("project_id")
    new_id = helpers.user_by_username(
        request.json.get("username")
    )['user']['ref'].id()
    
    if helpers.add_user(new_id, project_id):
        return jsonify({ 
            "msg": "Successsfully added user to this project" 
        }), 201

    return jsonify({ 
        "msg": "Could not add user to this project" 
    }), 500

@app.route("/projects/get_project_from_id", methods=["GET"])
def project_by_id():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401

    project = helpers.project_by_id(request.json.get("project_id"))

    if (project["user_id"] != token["id"]):
        return jsonify({
            "success": False,
            "msg": "We couldn't verify you."
        }), 401
    else:
        return jsonify({
            "success": True,
            "data": project
        }), 200

@app.route("/projects_by_region")
def projects_by_region():
    pass

@app.route("/submit_project", methods=["POST"])
def submit():
    # # token_response = helpers.validate_jwt(request)
    # if not token_response["success"]:
    #     return jsonify(token_response), 401
    # if helpers.delete_project(request.json.get("project_id")):
    #     return jsonify({
    #         "success": True,
    #     })

    

    if helpers.submit_project(request.json.get("project_id")):
        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False,
        "msg": "Something went wrong deleting that project."
    })