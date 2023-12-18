# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import psycopg2
from pymongo import MongoClient
import streamlit as st
import toml
import os
import pandas as pd
from model import *
from datetime import datetime

# Define the database connection
# secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")
from database import get_db

mongo_client = MongoClient("mongodb+srv://radhakrishnanganapathy5:pnvGVTD7rM3kgFTN@radhakrishnan.cozk1ms.mongodb.net/youtube")
db = mongo_client['youtube']
channel_collection = db["channel_collection"]
playlist_collection = db["playlist_collection"]
video_collection = db["video_collection"]
comment_collection = db["comment_collection"]

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

def migration():
     try:
          # DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
          #               f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
          # DATABASE_URI = "postgres://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"
          # --------- Below DB_URI is for streamlit online deployment
          # DATABASE_URI =  "postgresql://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao" 
          DATABASE_URI =  "postgres://radhakrishnan:1D1sWtcoTVBB7U26tX2EOJ9a1Q4zu82x@dpg-ckp2oi8ujous738qgcdg-a.oregon-postgres.render.com:5432/guviproject"
     
     
     
          engine = create_engine(DATABASE_URI, echo=True)
          Base.metadata.create_all(engine)
          Session = sessionmaker(bind=engine)
          db = Session()
     
          comment_data = list(comment_collection.find())
          for document in comment_data:
               user_id = document['user_id']
               db_return = db.query(Comment).filter(Comment.user_id == user_id).first()
               if not db_return :
                    comment = Comment(
                    username=document['userName'],
                    user_id=document['user_id'],
                    comment_text=document['comment_text'],
                    video_id=document['video_id']
                    )
                    db.add(comment)
     
          video_data = list(video_collection.find())
          for data in video_data:
               video_id = data['video_id']
               db_return = db.query(Videos).filter(Videos.video_id == video_id).first()
               if not db_return:
                    video = Videos(
                    video_id = data['video_id'],
                    channel_id = data['channel_id'],
                    video_title = data['video_title'],
                    video_description = data['video_description'],
                    dislike_count = data['dislike_count'],
                    duration = data['duration'],
                    favorite_count = data['favorite_count'],
                    comment_count = data['comment_count'],
                    like_count = data['like_count'],
                    published_date = data['published_date'],
                    playlist_id = data['playlist_id'],
                    view_count = data['view_count']
                    )
                    db.add(video)
          channel_data = list(channel_collection.find())
          for data in channel_data:
               channel_id = data['channel_id']
               db_return = db.query(Channel).filter(Channel.channelid == channel_id).first()
               if not db_return:
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
                    db.add(channel)
          playlist_data = list(playlist_collection.find())
          for data in playlist_data:
               playlist_id = data['playlist_id']
               db_return = db.query(Playlist).filter(Playlist.channel_id == playlist_id).first()
               if not db_return:
                    playlist = Playlist(
                    channel_id = data['channel_id'],
                    playlist_id = data['playlist_id'],
                    playlist_title = data['playlist_title'],
                    playlist_description = data['playlist_description'],
                    )
                    db.add(playlist)
                    # playlist_coll = db.query(Playlist).all()
                    # st.write(playlist_coll)
          db.commit()
          db.close()
          mongo_client.close()
     except Exception as e:
          st.write(e)
