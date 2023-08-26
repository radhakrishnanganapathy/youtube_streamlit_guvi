# mongodb_connection.py
from pymongo import MongoClient

def save_to_mongodb_channel(data,mongodbURL):
    client = MongoClient(mongodbURL)
    db = client['youtube']
    channel_collection = db["channel_collection"]
    channel_collection.insert_many(data)
    client.close()

def save_to_mongodb_playlist(data,mongodbURL):
    client = MongoClient(mongodbURL)
    db = client['youtube']
    playlist_collection = db["playlist_collection"]
    playlist_collection.insert_many(data)
    client.close()

def save_to_mongodb_videos(data,mongodbURL):
    client = MongoClient(mongodbURL)
    db = client['youtube']
    video_collection = db["video_collection"]
    video_collection.insert_many(data)
    client.close()

def get_videos_id(mongodbURL):
    video_ids = []
    client = MongoClient(mongodbURL)
    db = client['youtube']
    video_collection = db["video_collection"]
    # data = video_collection.find()
    cursor = video_collection.find({}, {"video_id": 1})

# Iterate over the cursor to extract video IDs and add to the list
    for document in cursor:
        video_ids.append(document["video_id"])
    return video_ids

def save_to_mongodb_comments(data,mongodbURL):
    client = MongoClient(mongodbURL)
    db = client['youtube']
    comment_collection = db["comment_collection"]
    comment_collection.insert_many(data)
    client.close()
















    
    
