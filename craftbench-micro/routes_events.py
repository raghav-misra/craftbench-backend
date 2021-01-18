from faunadb.query import events
import helpers
from flask import request, jsonify

from main import app

# Create a new event
@app.route("/create_event", methods=["POST"])
def create_event():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    if helpers.make_event(
            request.json.get("data")
        ):
        return { "message": "Successfully made a new event." }
        
    return { "error": "Could not create that event." }

@app.route("/update_event", methods=["POST"])
def update_event():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    if helpers.update_event(
            request.json.get("event_id"), 
            request.json.get("data")
        ):
        return { "message": "Succesfully updated event" }

    return { "event": "Could not update that event." }

# Add an activity to an event (The activity contains a user_id and damage)
@app.route("/add_activity", methods=["POST"])
def add_activity():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    add_status = helpers.add_activity(
        request.json.get("activity"),
        request.json.get("event_id")
    )
    if add_status == 'd':
        return { "message": "Successfully added that activity and deleted the event." }
    elif add_status == 'u':
        return { "message": "Successfully added that activity." }
    return { "error": "Could not add that activity." }

@app.route("/delete_event", methods=["POST"])
def delete_event():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    if delete_event(
            request.json.get("event_id")
        ):
        return { "message": "Successfully deleted that event." }

    return { "error": "Could not delete that event." }

@app.route("/event_by_region_name", methods=["POST"])
def event_by_region_name():
    token_response = helpers.validate_jwt(request)
    if not token_response["success"]:
        return jsonify(token_response), 401
    return helpers.event_by_region_name(
        request.json.get("region")
    )