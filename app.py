from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient


client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")

# user_id = 287839756335710720

# user = client.query(
#     q.get(
#         q.match(
#             q.index("user_id_by_users"),
#             "rathul_anand"
#         )
#     )
# )

# print("User ID:", user["ref"].id())

# id = user["ref"].id()

# projects = client.query(
#     q.get(
#         q.match(
#             q.index("projects_by_user_id"),
#             int(id)
#         )
#     )
# )

# print("Projects: ", projects)

# '''
# type Project {
#   name: String!
#   desc: String!
#   tasks: [Task]
#   owner: User!
#   event: event @relation
#   access: [Users] @relation
# }

# type User{
#   username: String! @unique
#   email: String! @unique
#   name: String
#   project: [Project] @relation
# }

# type event{
#   type: String!
#   base:Int!
#   resistance: Int!
#   activityLog:[String]
#   region:String!
# }
# '''
