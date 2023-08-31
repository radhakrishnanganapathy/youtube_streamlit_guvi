# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.dialects.postgresql import psycopg2
from pymongo import MongoClient
import streamlit as st
import toml
import os
import pandas as pd
from sqlalchemy.orm import Session

# Define the database connection
# secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")

secrets = toml.load(".streamlit/secrets.toml")
# secrets = toml.load(secrets_path)

DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
                   f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
# DATABASE_URI = "postgres://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"
engine = create_engine(DATABASE_URI, echo=True)

# Create a base class for declarative models
Base = declarative_base()

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
     subscribers = Column(Integer,nullable = False, index = True)
     view_count = Column(Integer,nullable = False, index = True)
     total_videos = Column(String(255),nullable = False, index = True)
     publishedAt = Column(Date)
     Country = Column(String(255))
     description = Column(Text)

     def name_of_all_channel_videos(db:Session):
           db_return = db.query(Channel.channelname,Videos.video_title).filter(Channel.channelid == Videos.channel_id).all()
           return db_return
     def most_videos_in_channel(db:Session):
           db_return = db.query(Channel.channelname,Channel.view_count).order_by(Channel.view_count.desc()).first()
           return db_return

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
     comment_count = Column(Integer,nullable = False, index = True)
     like_count = Column(Integer,nullable = False, index = True)
     playlist_id = Column(String(255))
        