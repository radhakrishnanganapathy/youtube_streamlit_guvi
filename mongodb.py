# mongodb_connection.py
from pymongo import MongoClient
import os 
import toml
secrets = toml.load(".streamlit/secrets.toml")

def save_to_mongodb_channel(data):
    # connection_string = os.environ.get("MONGODB_URI")
    # client = MongoClient(secrets["mongodb"]["connection_url"])
    client = MongoClient("mongodb+srv://radhakrishnanganapathy5:pnvGVTD7rM3kgFTN@radhakrishnan.cozk1ms.mongodb.net/youtube")
    # client = MongoClient(mongodbURL,
    # serverSelectionTimeoutMS=5000,  # Set a timeout value in milliseconds
    # connectTimeoutMS=5000,         # Set a connection timeout value in milliseconds
    # retryWrites=True  )
    db = client['youtube']
    channel_collection = db["channel_collection"]
    channel_collection.insert_many(data)
    client.close()

def save_to_mongodb_playlist(data):
    client = MongoClient(secrets["mongodb"]["connection_url"])
    # client = MongoClient(mongodbURL)
    db = client['youtube']
    playlist_collection = db["playlist_collection"]
    playlist_collection.insert_many(data)
    client.close()

def save_to_mongodb_videos(data):
    # client = MongoClient(mongodbURL)
    client = MongoClient(secrets["mongodb"]["connection_url"])
    db = client['youtube']
    video_collection = db["video_collection"]
    video_collection.insert_many(data)
    client.close()

def get_videos_id():
    video_ids = []
    client = MongoClient(secrets["mongodb"]["connection_url"])
    # client = MongoClient(mongodbURL)
    db = client['youtube']
    video_collection = db["video_collection"]
    # data = video_collection.find()
    cursor = video_collection.find({}, {"video_id": 1})

# Iterate over the cursor to extract video IDs and add to the list
    for document in cursor:
        video_ids.append(document["video_id"])
    return video_ids

def save_to_mongodb_comments(data):
    client = MongoClient(secrets["mongodb"]["connection_url"])
    # client = MongoClient(mongodbURL)
    db = client['youtube']
    comment_collection = db["comment_collection"]
    comment_collection.insert_many(data)
    client.close()
















    
    
