from pymongo import MongoClient
 
# MongoDB 연결
client = MongoClient("mongodb://localhost:27017")
db = client.finance
household = db.household

household.delete_many({})