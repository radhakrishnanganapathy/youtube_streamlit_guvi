from sqlalchemy import Column, Integer, String, Text, func
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
        def most_video_uploded(db:Session):
             db_return = db.query(Channel.channelname,Channel.total_videos).order_by(Channel.total_videos.desc()).limit(1).all()
            #  data = {
            #       "channel_name" : db_return.channelname,
            #         "video_count" : db_return.video_count
            #  }
             return db_return
        def top_ten_viewed(db:Session): #top ten views
             db_return = db.query(Channel.channelname,Videos.video_title,Videos.like_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.like_count.desc()).limit(10).all()
             return db_return
        
        def comments_of_each_video(db:Session):
             datas = []
             db_return = db.query(Videos.comment_count, Videos.video_title).all()
             for i in db_return:
                  data = {
                       "video_title" : i.video_title,
                       "comment_count": i.comment_count
                  }
                  datas.append(data)
             return datas
        def top_likes(db:Session):
             db_return = db.query(Channel.channelname,Videos.video_title,Videos.like_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.like_count.desc()).limit(1).all()
             return db_return
        
        def most_like_and_dislike(db:Session):
             db_return = db.query(Channel.channelname,Videos.video_title,Videos.like_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.like_count.desc()).all()
             return db_return
        
        def total_like_of_channel(db:Session): #view $ likes
             db_return = db.query(Channel.channelname,Videos.video_title,Videos.like_count).filter(Channel.channelid == Videos.channel_id).order_by(Videos.like_count.desc()).all()
             return db_return
        
        def published_year(db:Session):
            #  db_return = db.query(Channel.channelname, Channel.published_year).filter(Channel.published_year > )
             db_return = db.query(Channel).first()
            #  data = [item.publishedAt for item in  db_return]
             data = {
                 "data" : db_return.publishedAt
            }
             return data
             
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

class PlayList(Base):
    __tablename__ = 'playlist'
    id = Column(Integer,primary_key=True)
    channel_id = Column(String(255))
    playlist_id = Column(String(255))
    playlist_title = Column(String(255))
    playlist_description = Column(Text)
    def migrate_playlist(db:Session):
        for data in playlist_collection.find():
            # st.write(data)
            playlist = PlayList(
            channel_id = data['channel_id'],
            playlist_id = data['playlist_id'],
            playlist_title = data['playlist_title'],
            playlist_description = data['playlist_description'],
            )
            db.add(playlist)
            playlist_coll = db.query(PlayList).all()
            st.write(playlist_coll)

class Comment(Base):
        __tablename__ = 'comments'
        id = Column(Integer, primary_key=True)
        username = Column(String(255))
        user_id = Column(String(255))
        comment_text = Column(Text)
        video_id = Column(String(255))

        def migrate_comments(db:Session):
             for document in comment_collection.find():
                comment = Comment(
                    username=document['userName'],
                    user_id=document['user_id'],
                    comment_text=document['comment_text'],
                    video_id=document['video_id']
                )
                db.add(comment)
             db.commit()
             return comment