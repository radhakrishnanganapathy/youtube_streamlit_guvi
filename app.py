import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError
# from googleapiclient.errors import ConfigurationError

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
        if api_key is None:
            return (st.write("enter api"))
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
    # except HttpError as e:
    #     st.write("Quota. Please wait and try again later", e)
    #     return handle_exception(e)
    except Exception as e:
        st.write("your db url is invalid or Please enter your db url ", e)
        # return handle_exception(ce)
    # except DefaultCredentialsError as dce:
    #     st.write("Please enter your API Key", dce)
    #     return handle_exception(dce)
    # except KeyError as ke:
    #     st.write("Please enter any channel id")
    #     return handle_exception(ke)
    
    
#'''-----------------------------PlayList info-------------------------------------------'''

def get_playlist_info(youtube,api_key,channel_id,resultLimit,pageLimit):
    try:
        playlist_info = []
        next_page_token = None
        for channelID in channel_id:
            for i in range(pageLimit):
                playlist_response = youtube.playlists().list(
                    part = 'snippet',
                    channelId = channelID,
                    maxResults = resultLimit,
                    pageToken = next_page_token
                ).execute()
                if "items" in playlist_response:
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
                else :
                    data = {
                        "channel_id" : channelID,
                        "playlist_id" : None,
                        "playlist_title" :"playlist not created by user",
                        "playlist_description":None
                    }
                    playlist_info.append(data)
                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break
        save_to_mongodb_playlist(playlist_info)
        st.header("Playlist info:")
        st.write(pd.DataFrame(playlist_info))
    # except HttpError as e:
    #     st.write("Quota exceeded. Please wait and try again later")
    #     return handle_exception(e)
    except Exception   as ce:
        st.write("your db url is invalid or Please enter your db url ", ce)
    # except DefaultCredentialsError as dce:
    #     st.write("Please enter your API Key", dce)
    # except KeyError as ke:
    #     st.write("Please enter any channel id")

#'''-----------------------------Video info-------------------------------------------'''


def get_video_info(youtube,api_key,channel_id,resultLimit,pageLimit):
    try:
        next_page_token = None
        video_info = []
        for channelID in channel_id:
            for i in range(pageLimit):
                video_response = youtube.search().list(
                    part="id",
                    channelId = channelID,
                    maxResults = resultLimit,
                    type = "video",
                    pageToken = next_page_token
                ).execute()
                if "items" in video_response:
                    videos.extend(video_response["items"])
                
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
                    playlist_response = youtube.playlistItems().list(
                        part = "snippet",
                        id = videoID,
                        maxResults = resultLimit,
                    ).execute()
                    if "items" in playlist_response:
                        if playlist_response["items"]:
                            playlist_id = playlist_response["items"][0]["snippet"]["playlistId"]
                        else:
                            playlist_id = None
                    else:
                        playlist_id = None

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
    # except HttpError as e:
    #     st.write("Quota exceeded. Please wait and try again later")
    #     return handle_exception(e)
    except Exception   as ce:
        st.write("your db url is invalid or Please enter your db url ", ce)
    # except DefaultCredentialsError as dce:
    #     st.write("Please enter your API Key", dce)
    # except KeyError as ke:
    #     st.write("Please enter any channel id")
    
#'''-----------------------------Comment info-------------------------------------------'''

def get_comment_info(youtube,api_key,resultLimit):
    try:    
        video_id = get_videos_id()
        # videoss =['dD4GyhSQMR0']
        next_page_token = None
        comments_info = []
        comments = []
        for videoID in video_id:
            comment_response = youtube.commentThreads().list(
                part = "snippet",
                videoId = videoID,
                maxResults=resultLimit,
                pageToken = next_page_token
            ).execute()

            if "items" in comment_response and len(comment_response["items"])>0:
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
            else:
                data = {
                    "video_id" :videoID,
                    "userName" :None,
                    "user_id" :None,
                    "comment_text":"no comment for this video"
                }
                comments_info.append(data)

            if "nextPageToken" in comment_response:
                next_page_token = comment_response["nextPageToken"]
            else:
                break
        save_to_mongodb_comments(comments_info)
        st.header("Comments info:")
        st.write(pd.DataFrame(comments_info))
    # except HttpError as e:
    #     st.write("Quota exceeded. Please wait and try again later",e)
    #     return handle_exception(e)
    except Exception   as ce:
        st.write("your db url is invalid or Please enter your db url ", ce)
    # except DefaultCredentialsError as dce:
    #     st.write("Please enter your API Key", dce)
    # except KeyError as ke:
    #     st.write("Please enter any channel id")

api_key = st.sidebar.text_input("API KEY :")
channel_ids = st.sidebar.text_input("Channel ID :")
resultLimit = st.sidebar.number_input("Result Limt : ",value=0, step=1, format="%d")
pageLimit = st.sidebar.number_input("Page Limt : ",value=0, step=1, format="%d")
# mongodbURL = st.sidebar.text_input("MongoDb Url : ",placeholder="e.g : mongodb://localhost:27017/")
# MysqlUrl = st.sidebar.text_input("MySQL Url : ",placeholder="e.g. mysql://username:password@localhost:port/dbname")


videos = []
# playlist_max_page = st.sidebar.number_input("playlist_max_page_no :")
channel_id = channel_ids.split(",")
youtube = build('youtube','v3', developerKey=api_key)
st.sidebar.write("Here some ChannelIds")
data = ['UC6rE8DCMFYDcxOlvYG3JtBw,UCTIuWYnWo-7CmYZqXD8WFRA,UCGR1yjrScqezllTc2gsAIuA,UCwVkm1JU8MZbCITwfwIVQrg,UCYPbbwjbPkXEYx_xZEFvAJg,UCDJRFCKmzfISSFxO4lvCmag,UCPckFo2VPsPJBi2Xz3pk0pA,UCM9zAxQAC7erc9A0xqFg23g,UCXSgUVRaGyjc1Z3wqlsw7Aw,UC8Nt97MD1kNEobv25LqGIqA'],# mr.tamilan
st.sidebar.write(data)
# for channelID in channel_id:
youtube_Channel_analysis(youtube,api_key,channel_id)
get_playlist_info(youtube,api_key,channel_id,resultLimit,pageLimit)
get_video_info(youtube,api_key,channel_id,resultLimit,pageLimit)
get_comment_info(youtube,api_key,resultLimit)
# migrate_to_mysql()
