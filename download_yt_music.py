#!/usr/bin/env python

# ---- Imports -----------------------------------------------------------------
# Batteries
import argparse
import logging
import subprocess
import sys
import pathlib

# Plugs
import eyed3
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL

# local
from utils import get_music_path
# ---- Parameters --------------------------------------------------------------
YT_OWNER_ID='https://music.youtube.com'
YT_MUSIC_URL_PREFIX=YT_OWNER_ID+'/watch?v='
YT_MUSIC_AUTH_FILE='/home/sobh/.secret/yt_music-oauth.json'
# ---- Utilities ---------------------------------------------------------------
# ---- Command Line Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', default=0, action='count',
                    help='Verbosity level.')
args = parser.parse_args()
# ---- Logging -------------------------
v_levels = (logging.WARNING, logging.INFO, logging.DEBUG)
v_level = v_levels[min(args.verbose, len(v_levels) - 1)]
v_level = logging.INFO
logging.root.setLevel(logging.ERROR)
logging.basicConfig(
                     format=
                     '%(levelname)-8s: '
                     '%(module)25s.%(funcName)-25s %(lineno)4d | %(message)s'
                     )
logger = logging.getLogger(__name__)
logger.setLevel(v_level)

# ---- Function ----------------------------------------------------------------
def tag_yt_song(yt_song, fname):
    # logger.info(f"Tagging Track {ytid} in Library: {artist:30} - {title}")
    ytid = yt_song['videoId']
    audio_file = eyed3.load(fname)
    audio_file.tag.title  = yt_song['title']
    audio_file.tag.artist = yt_song['artists'][0]['name']
    audio_file.tag.album  = yt_song['album']['name']
    audio_file.tag.audio_source_url = YT_MUSIC_URL_PREFIX+ytid
    audio_file.tag.unique_file_ids.set(ytid, YT_OWNER_ID)
    audio_file.tag.save()




def download_yt_song(dir, track_ids):
    output_template = f'{dir}/%(id)s.%(ext)s'
    ytd_opt = {
            'extract_flat': 'discard_in_playlist',
            'final_ext': 'mp3',
            'format': 'bestaudio/best',
            'fragment_retries': 10,
            'ignoreerrors': 'only_download',
            'outtmpl': {'default': output_template},
            'postprocessors': [{'key': 'FFmpegExtractAudio',
                                'nopostoverwrites': False,
                                'preferredcodec': 'mp3',
                                'preferredquality': '0'},
                               {'key': 'FFmpegConcat',
                                'only_multi_video': True,
                                'when': 'playlist'}
                               ],
            'retries': 10,
            'writethumbnail': True
            }
    ytd = YoutubeDL(ytd_opt)
    ytd.download(track_ids)



# ---- Main --------------------------------------------------------------------
try:
    music_dir = get_music_path()
except FileNotFoundError:
    logger.critical("Unable to determine the 'Music Directory'.")
    sys.exit(-1)
new_music_dir = music_dir.joinpath('new')

if not new_music_dir.is_dir():
    if new_music_dir.exists():
        logger.critical(f"New Music Directory: '{new_music_dir}' exists, and is not a directory.")
        sys.exit(-1)
    logger.info(f"Will Create the new music directory: '{new_music_dir}'")
    new_music_dir.mkdir()

# Go through all music files, and get YouTube Video ID if available
music_file_names = list(music_dir.glob('**/*.mp3'))
audio_files = map(eyed3.load, music_file_names)
tags = [ af.tag for af in audio_files ]
yt_id_frames = [ tag.unique_file_ids.get(YT_OWNER_ID) for tag in tags ]
local_yt_ids = [ id_frame.uniq_id.decode() for id_frame in yt_id_frames if id_frame is not None ]



# Get YouTubeMusic Library Tracks
ytm = YTMusic(auth=YT_MUSIC_AUTH_FILE)
yt_songs = list(ytm.get_library_songs(limit=None))
missing_songs = { song['videoId']:song for song in yt_songs if song['videoId'] not in local_yt_ids}
# print('Missing Songs:')
# for song in missing_songs.values():
#     print(f"{song['videoId']}: {song['artists'][0]['name']:60} - {song['title']}")
# sys.exit(0)

# Download Tracks
download_yt_song(new_music_dir.absolute(), missing_songs.keys())

# Tag the downloaded Tracks
new_files = list(new_music_dir.glob('*.mp3'))
for track_file in new_files:
    ytid = track_file.stem
    if ytid in missing_songs.keys():
        tag_yt_song(missing_songs[ytid], track_file)
