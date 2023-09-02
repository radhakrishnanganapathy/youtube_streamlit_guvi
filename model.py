# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text, Date, Interval, func
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

# DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
#                    f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
DATABASE_URI = "postgres://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"
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
     total_videos = Column(Integer,nullable = False, index = True)
     publishedAt = Column(Date)
     Country = Column(String(255))
     description = Column(Text)

     def name_of_all_channel_videos(db:Session):
           db_return = db.query(Channel.channelname,Videos.video_title).filter(Channel.channelid == Videos.channel_id).all()
           return db_return
     def most_videos_in_channel(db:Session):
          #  db_return = db.query(Channel.channelname,func.max(Channel.view_count).label("max_total_videos")).first()
           db_return = db.query(Channel.channelname, func.max(Channel.total_videos).label("max_total_videos")).group_by(Channel.channelname).order_by(func.max(Channel.total_videos).desc()).first()
           return db_return
     def top_most_viewd_video(db:Session):
           data = []
           db_return = db.query(Channel.channelname, Videos.video_title, Videos.view_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.like_count.desc()).limit(10).all()
           for i in db_return:
               report = {
                    "channel_name" : i[0],
                    "video_title" : i[1],
                    "view_count" : i[2]
               }
               data.append(report)
           return data
     def comment_of_each_channel(db:Session):
           data = []
           db_return = db.query(Channel.channelname, Videos.video_title, Comment.comment_text).filter(Channel.channelid == Videos.channel_id).filter(Videos.video_id == Comment.video_id).all()
           for i in db_return:
                 report = {
                       "channel_name" : i[0],
                       "video_title" : i[1],
                       "comment" : i[2]
                 }
                 data.append(report)
           return data
     def most_like_of_video(db:Session):
           data = []
           db_return =db.query(Channel.channelname, Videos.video_title, Videos.like_count).filter(
                 Channel.channelid == Videos.channel_id
           ).order_by(Videos.like_count.desc()).all()
           for i in db_return:
                 report = {
                       "channel_name" : i[0],
                       "video_title" : i[1],
                       "like_count" : i[2]
                 }
                 data.append(report)
           return data
     def total_like_and_dislike(db:Session):
           data = []
           db_return = db.query(Channel.channelname,Videos.video_title,Videos.like_count,Videos.dislike_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.view_count.desc()).all()
           for i in db_return:
                 report = {
                       "channel_name" : i[0],
                       "video_title" : i[1],
                       "like_count" : i[2],
                       "dislike" : i[3]
                 }
                 data.append(report)
           return data
          
     def number_of_like(db:Session):
           data = []
           db_return = db.query(Channel.channelname, Channel.view_count).order_by(Channel.view_count.desc()).all()
           for i in db_return:
               report = {
                     "channel_name" : i[0],
                     "view_count" : i[1]
               }
               data.append(report)
           return data
     def published_year_two_thousand_twentytwo(db:Session):
           data = []
           db_return = db.query(Channel.channelname, Channel.publishedAt).filter(Channel.publishedAt > '2020-01-01').filter(Channel.publishedAt < '2020-12-31').order_by(Channel.publishedAt.asc()).all()
           for i in db_return:
                 report = {
                       "channel_name" : i[0],
                       "published_date" : i[1]
                 }
                 data.append(report)
           return data
     def avg_duration(db:Session):
           data = []
           db_return = db.query(Channel.channelname, func.avg(Videos.duration).label("avg duration")).filter(Channel.channelid == Videos.channel_id).group_by(Channel.channelname).order_by("avg duration").all()
           for i in db_return:
                 report = {
                       "channelName" : i[0],
                       "Avg Duration" : i[1]
                 }
                 data.append(report)
           return data
     def max_comment(db:Session):
           data = []
           db_return = db.query(Channel.channelname, Videos.video_title, func.max(Videos.comment_count)).filter(Channel.channelid == Videos.channel_id).group_by(Channel.channelname, Videos.video_title).all()
           for i in db_return:
                 report = {
                       "chanel name" : i[0],
                       "video title" : i[1],
                       "video count" : i[2]
                 }
                 data.append(report)
           return data

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
     like_count = Column(Integer,nullable = True, index = True)
     dislike_count = Column(Integer,nullable = True, index = True)
     favorite_count = Column(Integer,nullable = True, index = True)
     duration = Column(Interval)
     comment_count = Column(Integer,nullable = True, index = True)
     published_date = Column(Date)
     playlist_id = Column(String(255))
     view_count = Column(Integer,nullable = True, index = True)
        