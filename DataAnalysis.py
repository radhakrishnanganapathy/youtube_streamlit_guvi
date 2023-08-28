from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import streamlit as st
Base = declarative_base()

mongo_client = MongoClient("mongodb+srv://radhakrishnanganapathy5:pnvGVTD7rM3kgFTN@radhakrishnan.cozk1ms.mongodb.net/youtube")
db = mongo_client['youtube']
channel_collection = db["channel_collection"]
playlist_collection = db["playlist_collection"]
video_collection = db["video_collection"]
comment_collection = db["comment_collection"]

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

        def channel_data_migrate(db:Session):
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
                db.add(channel)
            db.commit()
            db.refresh(channel)
            return channel
        def get_channel_name(db:Session):
            datas = []
            return_db = db.query(Channel.channelname,Videos.video_title).filter(Channel.channelid == Videos.channel_id).all()
            # return_db = db.query(Channel).all()
            print(return_db)
            for i in return_db:
                data = {
                    "channel_name" : i.channelname,
                    "video_name" : i.video_title
                }
                datas.append(data)
            return datas

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

        def migrate_video(db:Session):
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
                db.add(video)
            db.commit()
            db.refresh(video)
            return video