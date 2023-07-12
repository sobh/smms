#!/usr/bin/env python

# ---- Imports -----------------------------------------------------------------
# Batteries
import argparse
import logging
import sys
import pathlib

# Plugs
import eyed3
from ytmusicapi import YTMusic

# Local
from utils import get_music_path, get_song_slug


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

# ---- Main --------------------------------------------------------------------
try:
    music_dir = get_music_path()
except FileNotFoundError:
    logger.critical("Unable to determine the 'Music Directory'.")
    sys.exit(-1)

music_dir = music_dir.joinpath('arabic')

# Go through all music files
local_music_files = list(music_dir.glob('**/*.mp3'))
local_songs_slugs = { path.stem:path for path in local_music_files }
# for slug in local_songs_slugs:
#     print(slug)

# Get YouTubeMusic Library Songs
ytm = YTMusic(auth=YT_MUSIC_AUTH_FILE)
yt_songs = list(ytm.get_library_songs(limit=None))
for yt_song in yt_songs:
    yt_artist = yt_song['artists'][0]['name']
    yt_title = yt_song['title']
    yt_song_slug = get_song_slug(yt_artist, yt_title)

    # Check If the Youtube Music song matches the slug of a local file
    if yt_song_slug in local_songs_slugs.keys():
        local_song_file = local_songs_slugs[yt_song_slug]
        yt_id = yt_song['videoId']

        print(f"File {local_song_file.name:60} matches Youtube Music ID: {yt_id}. Will set the YoutTube Music ID for this file")
        audiofile = eyed3.load(local_song_file)
        audiofile.tag.unique_file_ids.set(yt_id, YT_OWNER_ID)
        audiofile.tag.save()

        # Temporary
        # new_songs_path = pathlib.Path('~/music/new').expanduser()
        # new_fname = new_songs_path / (yt_id + '.mp3')
        # if new_fname.is_file() :
        #     print(f"\tNew song file '{new_fname.absolute()}' exists")
        #     new_fname.unlink()


        # print(f"{yt_song_slug:60} : {yt_artist:60} - {yt_title:60} => Found in Local Library")
