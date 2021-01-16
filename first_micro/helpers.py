from flask import Flask, request, jsonify, render_template, redirect
from faunadb import query as q
from faunadb.client import FaunaClient

client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")

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

def create_project(project):
    user_id = 287839756335710733
    name = project["name"]
    desc = project["desc"]
    tasks = project["tasks"]

    client.query(
        q.create(
            "projects", {
                "data": {
                        "user_id": user_id,
                        "name": name, 
                        "desc": desc, 
                        "tasks": tasks
                    }
            }
        )
    )

def projects_by_username(username):
    user = client.query(
        q.get(
            q.match(
                q.index("user_id_by_users"),
                username
            )
        )
    )

    return client.query(
        q.get(
            q.match(
                q.index("projects_by_user_id"),
                int(user["ref"].id())
            )
        )
    )['data']