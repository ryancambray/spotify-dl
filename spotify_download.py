#!/usr/bin/python
from __future__ import unicode_literals
import urllib3
import urllib.request
from bs4 import BeautifulSoup
import youtube_dl
import spotipy
import spotipy.util as util
import config
import os, errno
import shutil

PYTHONIOENCODING="UTF-8"

# Scan my playlists, cache songs as it goes and move the song into the correct directory
# Spotify API
scope = config.spotify_scope
spotify_username = config.spotify_username
client_id = config.spotify_client_id
client_secret = config.spotfiy_client_secret

# PoolManager to make requests
http = urllib3.PoolManager()


def get_youtube_link(song_name):
    query = song_name.replace(" ", "+")
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        print ('https://www.youtube.com' + vid['href'], flush=True)
        song_to_dl = "https://www.youtube.com" + vid['href']
        download_song(song_to_dl)
        break

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...\n', flush=True)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '320'
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

def download_song(song_to_dl):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_to_dl])


token = util.prompt_for_user_token(username=spotify_username, client_id=client_id, client_secret=client_secret,
                                   redirect_uri="http://localhost:8090", scope=scope)
if token:
    sp = spotipy.Spotify(auth=token)

    list_of_all_playlists = sp.current_user_playlists()

    for playlist in list_of_all_playlists['items']:
        # If the owner is me, proceed to scrape the playlist

        playlist_link = playlist.get('href')
        if str(playlist_link).startswith("https://api.spotify.com/v1/users/cambraytheyido"):
            playlist_id = playlist.get('id')

            playlist_name = str(playlist.get('name'))
            print("Going through playlist: " + playlist_name + "\n", flush=True)

            try:
                os.makedirs(playlist_name)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            for filename in ('ffmpeg.exe', 'ffplay.exe', 'ffprobe.exe'):
                shutil.copyfile(filename, os.path.join(playlist_name, filename))

            os.chdir(playlist_name)

            playlist_scrape = sp.user_playlist(spotify_username, playlist_id)
            for track_extract in playlist_scrape['tracks']['items']:
                track_details = track_extract['track']
                artist_name = str(track_details['artists'][0].get('name'))
                track_name = str(track_details.get('name'))
                youtube_string_search = artist_name + " " + track_name
                youtube_string_search = str(youtube_string_search.encode('utf-8'))

                print("Searching youtube for: " + artist_name + " - " + track_name, flush=True)

                get_youtube_link(youtube_string_search)