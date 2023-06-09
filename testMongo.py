write a progam to test the connection to a mongodb database.
  
import pymongo
from pymongo import MongoClient
  
# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://seankearns:nKwxkkDBahivkrPD@cluster0.bg2ernm.mongodb.net/?retryWrites=true&w=majority")

