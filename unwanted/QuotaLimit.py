from googleapiclient.errors import QuotaExceeded, RateLimitExceeded
from googleapiclient.discovery import build

# Replace with your API key and the API you want to check


def check_quota(api_key, youtube):
    youtube = build(youtube, developerKey=api_key)
    
    try:
        # Make a request that you would normally make to the API
        # For example, here we are getting the list of playlists
        youtube.playlists().list(part="snippet", maxResults=1).execute()
        print("Quota is not exceeded.")
    except QuotaExceeded:
        st.write("Quota is exceeded.")
    except RateLimitExceeded:
        st.write("Rate limit is exceeded.")
    except Exception as e:
        st.write("An error occurred:", str(e))

'''
[mysql]
host = "localhost"
user = "root"
password = "root123"
database = "youtube"
'''