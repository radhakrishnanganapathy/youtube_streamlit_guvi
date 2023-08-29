import streamlit as st
from googleapiclient.discovery import build
from google.auth.exceptions import DefaultCredentialsError
from app import *
from DataAnalysis import *
from database import get_db, CreateTables
import pandas as pd
st.header("Youtube Channel Analysis - Radhakrishnan G")
pd.set_option('display.max_rows', None)

CreateTables()

try:
    api_key = st.sidebar.text_input("API KEY :")
    channel_ids = st.sidebar.text_input("Channel ID :")
    resultLimit = st.sidebar.number_input("Result Limt : ",value=0, step=1, format="%d")
    pageLimit = st.sidebar.number_input("Page Limt : ",value=0, step=1, format="%d")
    channel_id = channel_ids.split(",")
    youtube = build('youtube','v3', developerKey=api_key)
    st.sidebar.write("Here some ChannelIds")
    data = ['UC6rE8DCMFYDcxOlvYG3JtBw,UCTIuWYnWo-7CmYZqXD8WFRA,UCGR1yjrScqezllTc2gsAIuA,UCwVkm1JU8MZbCITwfwIVQrg,UCYPbbwjbPkXEYx_xZEFvAJg,UCDJRFCKmzfISSFxO4lvCmag,UCPckFo2VPsPJBi2Xz3pk0pA,UCM9zAxQAC7erc9A0xqFg23g,UCXSgUVRaGyjc1Z3wqlsw7Aw,UC8Nt97MD1kNEobv25LqGIqA'],# mr.tamilan
    st.sidebar.write(data)
except DefaultCredentialsError as dce:
    st.header("Please Enter your api key")

col1,col2,col3,col4 = st.columns(4)

if col1.button("channel info"):
    channel_return = youtube_Channel_analysis(youtube,api_key,channel_id)
    st.write(channel_return)
if col2.button("Video info"):
    video_return = get_video_info(youtube,api_key,channel_id,resultLimit,pageLimit)
    st.write(video_return)
if col3.button("Playlist info"):
    playlist_return = get_playlist_info(youtube,api_key,channel_id,resultLimit,pageLimit)
    clo4.write(playlist_return)
if col4.button("Comments info"):
    comment_return = get_comment_info(youtube,api_key,resultLimit)
    st.write(comment_return)

if st.button("1.channel data"):
        db = next(get_db())
        db_return = Channel.get_channel_name(db)
        st.write(pd.DataFrame(db_return))
if st.button("2.Most Video"):
     db = next(get_db())
     db_return = Channel.most_video_uploded(db)
     st.write(pd.DataFrame(db_return))
if st.button("3.Top 10 Video"):
     db = next(get_db())
     db_return = Channel.top_ten_viewed(db)
     st.write(pd.DataFrame(db_return))
if st.button("4.comment count"):
     db = next(get_db())
     db_return = Channel.comments_of_each_video(db)
     st.write(pd.DataFrame(db_return))

if st.button("5.Most Like"):
     db = next(get_db())
     db_return = Channel.top_likes(db)
     st.write(pd.DataFrame(db_return))

if st.button("6.Like and dislike"):
     db = next(get_db())
     db_return = Channel.most_like_and_dislike(db)
     st.write("Note: There no key value of dislike in statistaics item")
     st.write(pd.DataFrame(db_return))

if st.button("7.Published 2022"):
     db = next(get_db())
     db_return = Channel.published_year(db)
     st.write(pd.DataFrame(db_return))

    