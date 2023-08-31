import streamlit as st
from googleapiclient.discovery import build
from google.auth.exceptions import DefaultCredentialsError
from app import *
from database import get_db, CreateTables
import pandas as pd
from Migration import *
from model import *

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

col0,col1 = st.columns(2)
col0.write("Enter a APIKEY, ChannelIDS and page/data limit to get channel data and click here -->")
if col1.button("GET channel datas"):
    channel_return = youtube_Channel_analysis(youtube,api_key,channel_id)
    video_return = get_video_info(youtube,api_key,channel_id,resultLimit,pageLimit)
    playlist_return = get_playlist_info(youtube,api_key,channel_id,resultLimit,pageLimit)
    comment_return = get_comment_info(youtube,api_key,resultLimit)
    st.write(channel_return)
    st.write(video_return)
    st.write(playlist_return)
    st.write(comment_return)
col3,clo4 = st.columns(2)
col3.write("click here to migrate data from mongodb to mysql")
if clo4.button("Data migration"):
    migration()
    st.write("data Migration")

if st.button("1.Names of all the videos and their corresponding channels"):
    db = next(get_db())
    db_return = Channel.name_of_all_channel_videos(db)
    st.write(pd.DataFrame(db_return))

if st.button("2.Channels have the most number of videos, and how many videos do they have"):
     db = next(get_db())
     db_return = Channel.most_videos_in_channel(db)
     st.write(pd.DataFrame(db_return))

if st.button("3.Top 10 most viewed videos and their respective channels"):
     db = next(get_db())
     db_return = Channel.top_ten_viewed(db)
     st.write(pd.DataFrame(db_return))

if st.button("4.Comments were made on each video, and what are their corresponding video names"):
     db = next(get_db())
     db_return = Channel.comments_of_each_video(db)
     st.write(pd.DataFrame(db_return))

if st.button("5.Videos have the highest number of likes, and what are their corresponding channel names"):
     db = next(get_db())
     db_return = Channel.top_likes(db)
     st.write(pd.DataFrame(db_return))

if st.button("6.The total number of likes and dislikes for each video, and what are their corresponding video names"):
     db = next(get_db())
     db_return = Channel.most_like_and_dislike(db)
     st.write("Note: There no key value of dislike in statistaics item")
     st.write(pd.DataFrame(db_return))

if st.button("7.The total number of views for each channel, and what are their corresponding channel names"):
     db = next(get_db())
     db_return = Channel.published_year(db)
     st.write(pd.DataFrame(db_return))

if st.button("8.The names of all the channels that have published videos in the year 2022"):
     db = next(get_db())
     db_return = Channel.published_year(db)
     st.write(pd.DataFrame(db_return))

if st.button("9.The average duration of all videos in each channel, and what are their corresponding channel names"):
     db = next(get_db())
     db_return = Channel.published_year(db)
     st.write(pd.DataFrame(db_return))

if st.button("10.Videos have the highest number of comments, and what are their corresponding channel names"):
     db = next(get_db())
     db_return = Channel.published_year(db)
     st.write(pd.DataFrame(db_return))

    