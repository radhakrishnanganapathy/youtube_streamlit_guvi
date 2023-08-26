# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import MySQLdb
import streamlit as st

# Define the database connection
def migrate_to_mysql(mongodbURL,MysqlUrl):
    DATABASE_URI = MysqlUrl
    engine = create_engine(DATABASE_URI, echo=True)

    # Create a base class for declarative models
    Base = declarative_base()

    # Define the Comment class
    class Comment(Base):
        __tablename__ = 'comments'
        id = Column(Integer, primary_key=True)
        username = Column(String(255))
        user_id = Column(String(255))
        comment_text = Column(Text)
        video_id = Column(String(255))

    class Channel(Base):
        __tablename__ = 'channel'
        id = Column(Integer,primary_key=True)
        channelid = Column(String(255))
        channelname = Column(String(255))
        subscribers = Column(String(255),nullable = False, index = True)
        view_count = Column(String(255),nullable = False, index = True)
        total_videos = Column(String(255),nullable = False, index = True)
        publishedAt = Column(String(255))
        Country = Column(String(255))
        description = Column(Text)

    class Playlist(Base):
        __tablename__ = 'playlist'
        id = Column(Integer,primary_key=True)
        channel_id = Column(String(255))
        playlist_id = Column(String(255))
        playlist_title = Column(String(255))
        playlist_description = Column(Text)

    class Videos(Base):
        __tablename__ = 'videos'
        id = Column(Integer,primary_key=True)
        video_id = Column(String(255))
        video_title = Column(String(255))
        video_description = Column(Text)
        comment_count = Column(String(255),nullable = False, index = True)
        like_count = Column(String(255),nullable = False, index = True)
        playlist_id = Column(String(255))
        

    # Establish MongoDB connection
    mongo_client = MongoClient(mongodbURL)
    db = mongo_client['mydatabase']
    channel_collection = db["channel_collection"]
    playlist_collection = db["playlist_collection"]
    video_collection = db["video_collection"]
    comment_collection = db["comment_collection"]

    # Create a session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Migrate data from MongoDB to MySQL
    for document in comment_collection.find():
        comment = Comment(
            username=document['userName'],
            user_id=document['user_id'],
            comment_text=document['comment_text'],
            video_id=document['video_id']
        )
        session.add(comment)
    session.commit()
    
    for data in channel_collection.find():
        channel = Channel(
          channelid = data['channel_id'],
          channelname = data['channel_name'],
          subscribers = data['subscribers'],
          view_count = data['view_count'],
          total_videos = data['total_videos'],
          publishedAt = data['publishedAt'],
          Country = data['Country'],
          description = data['description']
        )
        session.add(channel)
    session.commit()

    for data in playlist_collection.find():
        playlist = Playlist(
          channel_id = data['channel_id'],
          playlist_id = data['playlist_id'],
          playlist_title = data['playlist_title'],
          playlist_description = data['playlist_description'],
        )
        session.add(playlist)
    session.commit()

    for data in video_collection.find():
        video = Videos(
          video_id = data['video_id'],
          video_title = data['video_title'],
          video_description = data['video_description'],
          comment_count = data['comment_count'],
          like_count = data['like_count'],
          playlist_id = data['playlist_id'],
        )
        session.add(video)
    session.commit()

    # Close the session
    session.close()
    mongo_client.close()
    return st.write("Data Saved Successully")