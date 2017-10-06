#!/usr/bin/python
from __future__ import unicode_literals
import youtube_dl
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#Youtube API
DEVELOPER_KEY = "AIzaSyA8kKPryTP_dowwQ4MoK368SfHtrpqFFz4"
YOUTUBE_API_SERVICE_NAME = "Auto download spotify tracks"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results).execute()

  videos = []

  for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
          videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                     search_result["id"]["videoId"]))
          print(videos)

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

youtube_link = 'link'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_link])