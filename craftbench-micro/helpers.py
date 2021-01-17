from faunadb import query as q
from faunadb.client import FaunaClient
from flask import jsonify
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

# Create a project
def create_project(project):
    # try:
    client.query(
        q.create(
            "projects", 
            {
                "data": project
            }
        )
    )
    return True # Project creation success
    # except:
    #     return False # Something fracked up

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
                int(user_by_username(username)['user']['ref'].id())
            )
        )
    )['data']

    projects = []

    for reference in project_refs:
        project_from_db = client.query(q.get(reference))
        projects.append({
            "data": project_from_db["data"],
            "ref": project_from_db["ref"].id()
        })
    
    return projects

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
    client.query(
        q.ref(
            q.collection("users"), 
            int(id)
        )
    )