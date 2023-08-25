# mongodb_connection.py
from pymongo import MongoClient

def save_to_mongodb_channel(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    channel_collection = db["channel_collection"]
    channel_collection.insert_many(data)
    client.close()

def save_to_mongodb_playlist(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    playlist_collection = db["playlist_collection"]
    playlist_collection.insert_many(data)
    client.close()

def save_to_mongodb_videos(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    video_collection = db["video_collection"]
    video_collection.insert_many(data)
    client.close()

def save_to_mongodb_comments(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    comment_collection = db["comment_collection"]
    comment_collection.insert_many(data)
    client.close()
















    
    
