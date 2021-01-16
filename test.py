from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient


client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")
user = client.query(
    q.get(
        q.match(
            q.index("user_id_by_users"),
            "rathul_anand"
        )
    )
)

print(
    # map(
        q.paginate(
            q.match(
                q.index("projects_by_user_id"),
                int(user["ref"].id())
            )
        )
    #     lambda x: q.get(q.var(x))
    # )
)

# print( client.query(
#     q.get(
#         q.match(
#             q.index("projects_by_user_id"),
#             int(user["ref"].id())
#         )
#     )
# ))