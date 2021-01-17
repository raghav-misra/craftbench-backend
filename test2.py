from werkzeug.security import check_password_hash, generate_password_hash
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient


client = FaunaClient(secret="fnAD_puLTVACDfjj6lEi151b_Zh3sXx83qaalyea")


'''
type Project {
  name: String!
  desc: String!
  tasks: [Task]
  owner: User!
  access: [Users] @relation
}

type User {
  username: String! @unique
  email: String! @unique
  name: String
  password_hash: String!
}

type Region {
    currentEvent: Event!
    eventData: { idk lmfao }
}
'''
