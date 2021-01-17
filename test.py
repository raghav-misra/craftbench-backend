from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient


client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")


project_id = int(287897702374572544)


client.query(
    q.get(
        q.ref(
            q.collection("projects"), 
            project_id
        )
    )
)
data = {
    "data": {
        "user_id": 287839756335710720,
        "shared_ids": [287910298753434120],
        "name": "Some Project 63",
        "desc": "Final Project 47",
            "tasks": [
            {
                "name": "Speech",
                "sub_tasks": [
                {
                    "name": "Intro",
                    "completed": True
                },
                {
                    "name": "Bodies",
                    "completed": True
                },
                {
                    "name": "Conclusion",
                    "completed": False
                }
                ]
            },
            {
                "name": "Powerpoint",
                "sub_tasks": [
                {
                    "name": "Intro",
                    "completed": False
                },
                {
                    "name": "Bodies",
                    "completed": False
                },
                {
                    "name": "Conclusion",
                    "completed": False
                }
                ]
            },
            {
                "name": "Present",
                "sub_tasks": [
                {
                    "name": "Speech",
                    "completed": False
                }
                ]
            }
            ]
        }
}
print(
    client.query(
        q.update(
            q.select("ref",
                client.query(
                    q.ref(
                        q.collection("projects"), project_id
                    )
                )
            ),
            data               
            
        )
    )
)
# Update(
#   Select("ref",
#     Get(
#       Match(Index("dept_by_deptno"), 10)
#     )
#   ),
#   {
#     data: { loc: "AUSTIN" }
#   }
# )