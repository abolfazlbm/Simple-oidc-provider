# from flask_pymongo.wrappers import Database
from flask_sqlalchemy import SQLAlchemy
# from app.resources.datastore.mongodb import Mongodb

sqlAlchemydb = SQLAlchemy()

# def mongo_init_db():
#     mongodb: Database = Mongodb().mongo.db
#     collections = mongodb.list_collection_names()
#     print(collections)
#     if "Location" not in collections:
#         mongodb.create_collection('Location')
#         print("Location Collection Created")
