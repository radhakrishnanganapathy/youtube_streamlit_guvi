from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import streamlit as st

from model import *
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
             
