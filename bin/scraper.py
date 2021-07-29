import pandas as pd
import os
from googleapiclient.discovery import build
from config import api_key
import argparse

data_path = os.getcwd() + "/results/"
yt = build('youtube', 'v3', developerKey=api_key)
base_video_url ="https://www.youtube.com/watch?v={}"

def list_upload_data(upload_id):
    videos = list()
    page_token = None
    while True:
        page_videos = yt.playlistItems().list(playlistId = upload_id, part='snippet', maxResults=50, pageToken=page_token).execute()
        videos += page_videos.get('items')
        page_token = page_videos.get('nextPageToken')
        if page_token is None:
            break
    return videos

def get_uploads_id(channel_id):
    # Retrieve the channel details and store in data
    channels_response = yt.channels().list(forUsername=channel_id, part='contentDetails').execute()
    # Get playlist ID
    for channel in channels_response.get('items', []):
        return channel.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
    return None

def to_video_ids(upload_data):
    videos = list()
    for video in upload_data:
        videos.append(
            video.get('snippet').get('resourceId').get('videoId')
        )
    return videos

def get_video_info(video_id):
    video_info = yt.videos().list(part='snippet,statistics', id=video_id).execute()
    for video in video_info.get('items'):
        return {
                "views": video.get('statistics').get('viewCount'),
                "likes": video.get('statistics').get('likeCount'),
                "title": video.get('snippet').get('title'),
                "date_published": video.get('snippet').get('publishedAt'),
                "url": base_video_url.format(video_id)
        }
    return None
    

def main(args):
    upload_playlist_id = get_uploads_id(args.channel)
    upload_data = list_upload_data(upload_playlist_id)
    video_ids = to_video_ids(upload_data)
    all_videos = list()
    for id in video_ids:
        res = get_video_info(id)
        all_videos.append(res)
    df = pd.DataFrame(all_videos)
    df.to_csv(data_path + args.channel + "_results.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('channel', type=str, help='Channel name')
    args = parser.parse_args()
    main(args)
