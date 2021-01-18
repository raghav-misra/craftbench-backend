import time
from faunadb import query as q
from faunadb.client import FaunaClient
from flask import jsonify
import jwt
import json
import os
from datetime import datetime, timezone

client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")

# Create user:
def create_new_user(user_data): 
    try:
        client.query(
            q.create(
                "users", {
                    "data": user_data
                }
            )
        )
        return True # Username creation success
    except:
        return False # Something fracked up

# Check if a username is taken:
def check_username_exists(username):
    try:
        client.query(
            q.get(
                q.match(
                    q.index("user_id_by_users"),
                    username
                )
            )
        )
        return True # Username is taken!
    except:
        return False # Username doesn't exist!

# Get userdata:
def user_by_username(username): 
    try: 
        user = client.query(
            q.get(
                q.match(
                    q.index("user_id_by_users"),
                    username
                )
            )
        )
        return {
            "success": True,
            "user": user
        }
    except:
        return {
            "success": False,
        }

# Delete a project from id
def delete_project(id):
    try:
        client.query(
            q.delete(
                client.query(
                    q.ref(
                        q.collection("projects"), 
                        id
                    )
                )
            )
        )
        return True
    except:
        return False

#Submit a projecet from id
def submit_project(project_id):
    add_activity(
        {
            "user_id": int(owner_id_from_project_id(project_id)),
            "damage": 100
        },
        event_id_from_project_id(project_id)
    )

    delete_project(project_id)

    return True

# Update the project at a given index to the new data
def update_project(project_id, data):
    try:
        client.query(
            q.replace(
                client.query(
                    q.ref(
                        q.collection("projects"), project_id
                    )
                ),
                {
                    "data": data
                }
                
            )
        )
        return True
    except:
        return False

# Add user to a project
def add_user(id, project_id):
        
    data = client.query(
        q.get(
            q.ref(
                q.collection("projects"), 
                project_id
            )
        )
    )['data']

    data['shared_ids'].append(id)

    update_project(project_id, data)

    return True
    
# Create a project
def create_project(request, user_id):
    try:
        return {
            "success": True,
            "data": client.query(
                q.create(
                    "projects", 
                    {
                        "data": {
                            "user_id": user_id,
                            "name": request.json.get("name"),
                            "desc": request.json.get("desc"),
                            "shared_ids": [],
                            "tasks": [],
                            "region": request.json.get("region").lower(),
                            "contribution": request.json.get("contribution"),
                            "contribution_type": request.json.get("contribution_type"),
                            "can_view_title": request.json.get("can_view_title"),
                        }
                    }
                )
            )
        } # Project creation success
    except Exception as e:
        print("CREATEPROJECTERROR", e)
        return {
            "success": False,
            "message": e
        } # Something fracked up

# Get userdata:
def user_by_username(username): 
    try: 
        user = client.query(
            q.get(
                q.match(
                    q.index("user_id_by_users"),
                    username
                )
            )
        )
        return {
            "success": True,
            "user": user
        }
    except:
        return {
            "success": False,
        }

# Return a list of projects by the username
def projects_by_username(username):
    project_refs = client.query(
        q.paginate(
            q.match(
                q.index("projects_by_user_id"),
                str(user_by_username(username)['user']['ref'].id())
            )
        )
    )['data']

    projects = []

    for reference in project_refs:
        project_from_db = client.query(q.get(reference))
        projects.append({
            project_from_db["data"]
        })
    
    return projects

# Update the project at a given index to the new data
def update_project(project_id, data):
    try:
        client.query(
            q.replace(
                client.query(
                    q.ref(
                        q.collection("projects"), project_id
                    )
                ),
                {
                    "data": data
                }
                
            )
        )
        return True
    except:
        return False

# Add user to a project
def add_user(id, project_id):
        
    data = client.query(
        q.get(
            q.ref(
                q.collection("projects"), 
                project_id
            )
        )
    )['data']

    data['shared_ids'].append(id)

    update_project(project_id, data)

    return True

# Get user by id:
def user_by_id(id):
    return client.query(
        q.get(
            q.ref(
                q.collection("users"),
                int(id)
            )
        )
    )['data']

# Get project by project id
def project_by_id(id):
    return client.query(
        q.get(
            q.ref(
                q.collection("projects"),
                int(id)
            )
        )
    )['data']

# Create a new event from the passed in data
def make_event(data):
    client.query(
        q.create(
            "event",
            {
                "data": data
            }
        )
    )
    return True

# Update the data of an event with the passed in data
def update_event(event_id, data):
    try:
        client.query(
            q.replace(
                client.query(
                    q.ref(
                        q.collection("event"), event_id
                    )
                ),
                {
                    "data": data
                }
                
            )
        )
        return True
    except:
        return False

# Add an activity to the activity log and do damage
def add_activity(activity, event_id):
    data = client.query(
        q.get(
            q.ref(
                q.collection("event"),
                event_id
            )
        )
    )['data']

    data['activityLog'].append(activity)
    data['base'] -= activity['damage']

    if data['base'] <= 0:
        delete_event(event_id)
        return 'd'
        
    update_event(event_id, data)
    return 'u'

# Get the owner's id from project id
def owner_id_from_project_id(project_id):
    return client.query(
        q.get(
            q.ref(
            q.collection("projects"),
            project_id
            )
        )
    )['data']['user_id']

# Delete an event based on its id
def delete_event(id):
    try:
        client.query(
            q.delete(
                client.query(
                    q.ref(
                        q.collection("event"),
                        id
                    )
                )
            )
        )
        return True
    except:
        return False

# Event by region name
def event_by_region_name(region):
    try:
        event = client.query(
            q.get(
                q.match(
                    q.index("event_by_region_name"),
                    region
                )
            )
        )['data']
        return {
            "success": True,
            "event": event
        }
    except:
        return {
            "success": False,
        }

# Get the event id by the project_id
def event_id_from_project_id(project_id):
    return int(
        client.query(
            q.get(
                q.match(
                    q.index("event_by_region_name"),
                    client.query(
                        q.get(
                            q.ref(
                            q.collection("projects"),
                            project_id
                            )
                        )
                    )['data']['region']
                )
            )
        )['ref'].id()
    )

# Authorize route:
def validate_jwt(request):
    try:
        token = request.headers["Authorization"].split("Bearer ")[1]
        id = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"])
        print(type(id))
        return {
            "success": True,
            "data": user_by_id(id["id"]),
            "id": id["id"]
        }
    except Exception as e:
        print(e)
        return { "success": False, "msg": "Whoops, we can't validate you. Please login." }