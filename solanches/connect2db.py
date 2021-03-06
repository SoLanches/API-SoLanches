import os

import pymongo
from dotenv import load_dotenv

load_dotenv()


SOLANCHES_DB_URI = os.getenv("SOLANCHES_DB_URI")

MONGO_CLIENT = pymongo.MongoClient(SOLANCHES_DB_URI)

DB = MONGO_CLIENT.SolanchesDB
DB.block_list.create_index("date", expireAfterSeconds=3600)
