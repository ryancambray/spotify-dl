#!/usr/bin/python
import urllib3
import urllib.request
from bs4 import BeautifulSoup

#PoolManager to make requests
http = urllib3.PoolManager()

query = 'deadmau5'
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, "html.parser")
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    print ('https://www.youtube.com' + vid['href'])

