#!/usr/bin/env python
#
# Description:  List songs in YouTube Music Library
#

# ---- Imports -----------------------------------------------------------------
import sys
from pathlib import Path
from ytmusicapi import YTMusic

# ---- Parameters --------------------------------------------------------------
YT_OWNER_ID='https://music.youtube.com'
YT_MUSIC_URL_PREFIX=YT_OWNER_ID+'/watch?v='

AUTH_FILE=Path('~/.secret/yt_music-oauth.json').expanduser()

# ---- Main --------------------------------------------------------------------
if not AUTH_FILE.is_file():
    print(f"Error: Unable to locate YouTube Music Authentication file in {AUTH_FILE}.")
    sys.exit(-1)

ytm = YTMusic(auth=AUTH_FILE)

songs = ytm.get_library_songs(limit=None)
# List Header
print("{:>6} | {:11} | {:30} | {:50} | {}".format('#', 'ID', 'Artist', 'Title','YouTube Music URL'))
print('-'*160)
# Songs List
for i, song in enumerate(songs):
    ytid = song['videoId']
    artist = song['artists'][0]['name']
    title  = song['title']
    url = YT_MUSIC_URL_PREFIX + ytid
    print(f"{i:6} | {ytid} | {artist:30} | {title:50} | {url}")
