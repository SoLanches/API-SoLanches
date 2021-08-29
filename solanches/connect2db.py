from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("SOLANCHES_DB_HOST")
db_port = int(os.getenv("SOLANCHES_DB_PORT"))

MONGO_CLIENT = MongoClient(db_host, db_port)

DB = MONGO_CLIENT.SolanchesDB
