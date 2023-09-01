import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError
from mongodb import *
from datetime import datetime
from dateutil import parser
import isodate

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
                "subscribers" : int(channel_request['items'][0]['statistics']['subscriberCount']),
                "view_count" : int(channel_request['items'][0]['statistics']['viewCount']),
                "total_videos" : int(channel_request['items'][0]['statistics']['videoCount']),
                "publishedAt" : parser.parse(channel_request['items'][0]['snippet']['publishedAt']).strftime('%Y-%m-%d'),
                "Country" : country,
                "description" : channel_request['items'][0]['snippet']['description']
            }
            channel_info.append(channel_data)
        save_to_mongodb_channel(channel_info)
        st.header("Channel info:")
        st.write(pd.DataFrame(channel_info))
    except Exception as e:
        st.write("Exception", e)
    
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
    except Exception   as ce:
        st.write(ce)
#'''-----------------------------Video info-------------------------------------------'''


def get_video_info(youtube,api_key,channel_id,resultLimit,pageLimit):
    try:
        videos = []
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
                    part="snippet,statistics,contentDetails",
                    id=videoID
                ).execute()

                if "items" in video_info_response:
                    video_snippet = video_info_response["items"][0]["snippet"]
                    video_statistics = video_info_response["items"][0]["statistics"]
                    video_content = video_info_response['items'][0].get('contentDetails',{})
                    
                    video_title = video_snippet["title"]
                    video_description = video_snippet["description"]
                    try:
                        comment_count = int(video_statistics["commentCount"])
                    except KeyError as ke:
                        comment_count = None
                    like_count = int(video_statistics["likeCount"])
                    dislike_count = int(video_statistics.get("dislikeCount",0))
                    favorite_count = int(video_statistics.get('favoriteCount',0))
                    duration = video_content['duration']#,"Duration not available")
                    duration_time = iso8601_to_hhmmss(duration)
                    # duration = video_response['items'][0]['contentDetails']['duration']
                    # published_date = video_statistics['publishedAt']
                    published_date = parser.parse(video_snippet['publishedAt']).strftime('%Y-%m-%d')
                    view_count = int(video_statistics['likeCount'])
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
                        "channel_id" : channelID,
                        "video_title":video_title,
                        "video_description" : video_description,
                        "comment_count" : comment_count,
                        "like_count" : like_count,
                        "dislike_count" : dislike_count,
                        "favorite_count" : favorite_count,
                        "published_date" : published_date,
                        "duration" : duration_time,
                        "playlist_id" :playlist_id,
                        "view_count" : view_count
                    }
                    video_info.append(data)
        save_to_mongodb_videos(video_info)
        st.header("Video info:")
        st.write(pd.DataFrame(video_info))
    except Exception as ce:
        st.write(ce)
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
    except Exception as e:
        return e

# migrate_to_mysql()
# videos_names()
# check_db_connection()
# video_channel()

def iso8601_to_hhmmss(duration):
    duration_obj = isodate.parse_duration(duration)
    hours, remainder = divmod(duration_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
