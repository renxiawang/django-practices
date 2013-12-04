from pymongo import MongoClient
from bson.objectid import ObjectId

def find_one_person(pid):
    return people.find_one({"_id": ObjectId(pid)})

def find_matches(keywords):
    return renwu.command("text", "people", search=keywords, limit=10)['results']

# connect to localhost MongoDB
client = MongoClient()

# Get the renwu database
renwu = client.renwu_fyp

# Get the baidu_sample collection
people = renwu.people