import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from googleapiclient.errors import HttpError
from mongodb import *
from mysql import *

st.header("Youtube Channel Analysis - Radhakrishnan G")
st.write("Welcome to your first Streamlit app!")


def handle_exception(e):
    if "quota" in str(e).lower():
        print("Quota exceeded. Please wait and try again later.")
    else:
        print("An error occurred:", str(e))
    return None

#'''-----------------------------Channel info-------------------------------------------'''

def youtube_Channel_analysis(youtube,api_key,channel_id):
    try:
        channel_info = []
        for channelID in channel_id:
            channel_request = youtube.channels().list(
                part= 'snippet,contentDetails,statistics',
                id = channelID
            ).execute()
            try:
                country = channel_request['items'][0]['snippet']['country']
            except KeyError:
                country = "Country information not available"
            channel_data = {
                "channel_id" : channelID,
                "channel_name" : channel_request['items'][0]['snippet']['title'],
                "subscribers" : channel_request['items'][0]['statistics']['subscriberCount'],
                "view_count" : channel_request['items'][0]['statistics']['viewCount'],
                "total_videos" : channel_request['items'][0]['statistics']['videoCount'],
                "publishedAt" : channel_request['items'][0]['snippet']['publishedAt'],
                "Country" : country,
                "description" : channel_request['items'][0]['snippet']['description']
            }
            channel_info.append(channel_data)
        save_to_mongodb_channel(channel_info)
        st.header("Channel info:")
        st.write(pd.DataFrame(channel_info))
    except HttpError as e:
        st.write("Quota exceeded. Please wait and try again later")
        return handle_exception(e)
    
#'''-----------------------------PlayList info-------------------------------------------'''

def get_playlist_info(youtube,api_key,channel_id):
    try:
        playlist_info = []
        next_page_token = None
        for channelID in channel_id:
            while True:
                playlist_response = youtube.playlists().list(
                    part = 'snippet',
                    channelId = channel_id,
                    maxResults = 50,
                    pageToken = next_page_token
                ).execute()
                for playlist in playlist_response["items"]:
                    playlist_id = playlist["id"]
                    playlist_title = playlist["snippet"]["title"]
                    playlist_description = playlist["snippet"]["description"]

                    data = {
                        "channel_id" : channelID,
                        "playlist_id" : playlist_id,
                        "playlist_title" :playlist_title,
                        "playlist_description":playlist_description

                    }
                    playlist_info.append(data)
                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break
        save_to_mongodb_playlist(playlist_info)
        st.header("Playlist info:")
        st.write(pd.DataFrame(playlist_info))
    except HttpError as e:
        st.write("Quota exceeded. Please wait and try again later")
        return handle_exception(e)

#'''-----------------------------Video info-------------------------------------------'''


def get_video_info(youtube,api_key,channel_id):
    try:
        next_page_token = None
        video_info = []
        for channelID in channel_id:
            while True:
                video_response = youtube.search().list(
                    part="id",
                    channelId = channelID,
                    maxResults = 50,
                    type = "video",
                    pageToken = next_page_token
                ).execute()
                if "items" in video_response:
                    videos.append(video_response["items"])
                
                next_page_token = video_response.get("nextPageToken")
                if not next_page_token:
                    break
            for video in videos:
                videoID = video["id"]["videoId"]

                video_info_response = youtube.videos().list(
                    part="snippet,statistics",
                    id=videoID
                ).execute()

                if "items" in video_info_response:
                    video_snippet = video_info_response["items"][0]["snippet"]
                    video_statistics = video_info_response["items"][0]["statistics"]

                    video_title = video_snippet["title"]
                    video_description = video_snippet["description"]
                    comment_count = video_statistics["commentCount"]
                    like_count = video_statistics["likeCount"]
                    playlist_id = None
                    playlist_response = youtube.playlistItems().list(
                        part = "snippet",
                        videoId = videoID,
                        maxresults = 50,
                    ).execute()
                    if "items" in playlist_response:
                        playlist_id = playlist_response["items"][0]["snippet"]["playlistId"]

                    data = {
                        "video_id" : videoID,
                        "video_title":video_title,
                        "video_description" : video_description,
                        "comment_count" : comment_count,
                        "like_count" : like_count,
                        "playlist_id" :playlist_id,
                    }
                    video_info.append(data)
        save_to_mongodb_videos(video_info)
        st.header("Video info:")
        st.write(pd.DataFrame(video_info))
    except HttpError as e:
        st.write("Quota exceeded. Please wait and try again later")
        return handle_exception(e)
    
#'''-----------------------------Comment info-------------------------------------------'''

def get_comment_info(youtube,api_key,videos):
    try:
        next_page_token = None
        comments_info = []
        comments = []
        for videoID in videos:
            comment_response = youtube.commentThreads().list(
                part = "snippet",
                videoId = videoID,
                maxResults=100,
                pageToken = next_page_token
            ).execute()

            if "items" in comment_response:
                comment_snippet = comment_response["items"][0]["snippet"]
                userName = comment_snippet["topLevelComment"]["snippet"]["authorDisplayName"]
                user_id = comment_snippet["topLevelComment"]["snippet"]["authorChannelId"]["value"]
                comment_text = comment_snippet["topLevelComment"]["snippet"]["textDisplay"]

                data = {
                    "video_id" :videoID,
                    "userName" :userName,
                    "user_id" :user_id,
                    "comment_text":comment_text
                }
                comments_info.append(data)
            if "nextPageToken" in comment_response:
                next_page_token = comment_response["nextPageToken"]
            else:
                break
        save_to_mongodb_comments(comments_info)
        st.header("Comments info:")
        st.write(pd.DataFrame(comments_info))
    except HttpError as e:
        st.write("Quota exceeded. Please wait and try again later")
        return handle_exception(e)

api_key = st.sidebar.text_input("API KEY :")
channel_ids = st.sidebar.text_input("Channel ID :")
videos = []
# playlist_max_page = st.sidebar.number_input("playlist_max_page_no :")
channel_id = channel_ids.split(",")
youtube = build('youtube','v3', developerKey=api_key)
st.sidebar.write("Here some ChannelIds")
data = ['UC6rE8DCMFYDcxOlvYG3JtBw,UCTIuWYnWo-7CmYZqXD8WFRA,UCGR1yjrScqezllTc2gsAIuA,UCwVkm1JU8MZbCITwfwIVQrg,UCYPbbwjbPkXEYx_xZEFvAJg,UCDJRFCKmzfISSFxO4lvCmag,UCPckFo2VPsPJBi2Xz3pk0pA,UCM9zAxQAC7erc9A0xqFg23g,UCXSgUVRaGyjc1Z3wqlsw7Aw,UC8Nt97MD1kNEobv25LqGIqA'],# mr.tamilan
st.sidebar.write(data)
# for channelID in channel_id:
youtube_Channel_analysis(youtube,api_key,channel_id)
get_playlist_info(youtube,api_key,channel_id)
get_video_info(youtube,api_key,channel_id)
get_comment_info(youtube,api_key,videos)

migrate_to_mysql()
