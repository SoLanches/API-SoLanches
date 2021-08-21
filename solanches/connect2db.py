from pymongo import MongoClient

MONGO_CLIENT = MongoClient("localhost", port=27017)

DB = MONGO_CLIENT.SolanchesDB
