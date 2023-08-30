# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.dialects.postgresql import psycopg2
from pymongo import MongoClient
import streamlit as st
import toml
import os
import pandas as pd
# Define the database connection
# secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")

secrets = toml.load(".streamlit/secrets.toml")
# secrets = toml.load(secrets_path)

def check_db_connection():
        DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
                   f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
        engine = create_engine(DATABASE_URI)
        try:
            connection = engine.connect()
            st.write("Database version:", connection)
            connection.close()
            st.write("Database connection is working.")
        except Exception as e:
            st.write("Error:", e)
            st.write("Database connection failed.")

def migrate_to_mysql():
    # DATABASE_URI = MysqlUrl
    DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
                   f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
    # DATABASE_URI = "postgres://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"
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
        channel_id = Column(String(255))
        video_id = Column(String(255))
        video_title = Column(String(255))
        video_description = Column(Text)
        comment_count = Column(String(255),nullable = False, index = True)
        like_count = Column(String(255),nullable = False, index = True)
        playlist_id = Column(String(255))
        

    # Establish MongoDB connection
    # mongo_client = MongoClient(secrets["mongodb"]["connection_url"])
    mongo_client = MongoClient("mongodb+srv://radhakrishnanganapathy5:pnvGVTD7rM3kgFTN@radhakrishnan.cozk1ms.mongodb.net/youtube")
    db = mongo_client['youtube']
    channel_collection = db["channel_collection"]
    playlist_collection = db["playlist_collection"]
    video_collection = db["video_collection"]
    comment_collection = db["comment_collection"]

    # Create a session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Migrate data from MongoDB to MySQL
    try:
        mongo_data = list(comment_collection.find())
        for document in mongo_data:
            user_id = document['user_id']
            db_return = db.query(Comment).filter(Comment.user_id == user_id).first()
            if not db_return :
                comment = Comment(
                    username=document['userName'],
                    user_id=document['user_id'],
                    comment_text=document['comment_text'],
                    video_id=document['video_id']
                )
                session.add(comment)
        # session.commit()
        
        for data in channel_collection.find():
            # st.write(data)
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
        # session.commit()

        for data in playlist_collection.find():
            # st.write(data)
            playlist = Playlist(
            channel_id = data['channel_id'],
            playlist_id = data['playlist_id'],
            playlist_title = data['playlist_title'],
            playlist_description = data['playlist_description'],
            )
            session.add(playlist)
        playlist_coll = session.query(Playlist).all()
        st.write(playlist_coll)

        # session.commit()

        for data in video_collection.find():
            video = Videos(
            video_id = data['video_id'],
            channel_id = data['channel_id'],
            video_title = data['video_title'],
            video_description = data['video_description'],
            comment_count = data['comment_count'],
            like_count = data['like_count'],
            playlist_id = data['playlist_id'],
            )
            session.add(video)
        session.commit()
    except Exception as e:
        st.write("Error during data migration:", e)
    # Close the session
    finally:
        session.close()
        mongo_client.close()
    # return st.write("Data Saved Successully")

