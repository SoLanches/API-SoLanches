import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("SOLANCHES_DB_HOST")
DB_PORT = int(os.getenv("SOLANCHES_DB_PORT"))

MONGO_CLIENT = pymongo.MongoClient(DB_HOST, DB_PORT)

DB = MONGO_CLIENT.SolanchesDB
