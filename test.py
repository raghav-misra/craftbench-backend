from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
# Deta, Fauna, Hoppscotch
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

def contributions_by_username(username):
    pass

client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")

username = "getprojecttest"

# projects = projects_by_username(username)
# for project in projects:
#     print(project)

# project_refs = client.query(
#     q.paginate(
#         q.match(
#             q.index("projects_by_contributor_id"),
#             int(user_by_username(username)['user']['ref'].id())
#         )
#     )
# )['data']

# print(project_refs)
# print(user_by_username(username)['user'])
# user = user_by_username(username)['user']['ref'].id()

# print(user)
# for thing in user:
#     print(str(thing) + ":   " + str(user[thing]))

print(
    # client.query(
    #     q.paginate(
            q.match(
                q.index("projects_by_contributor_id"),
                int(user_by_username(username)['user']['ref'].id())
            )
    #     )
    # )
)

project_refs = client.query(
    q.paginate(
        q.match(
            q.index("prµojects_by_user_id"),
            int(user_by_username(username)['user']['ref'].id())
        )
    )
)['data']