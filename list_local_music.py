#!/usr/bin/env python

# ---- Imports -----------------------------------------------------------------
# Batteries
import sys

# Plugs
import eyed3

# Local
from utils import get_music_path

# ---- Main --------------------------------------------------------------------
try:
    music_dir = get_music_path()
except FileNotFoundError:
    print("Unable to determine the 'Music Directory'.")
    sys.exit(-1)


# Go through all music files
music_files = list(music_dir.glob('**/*.mp3'))
# List Header
print("{:>6} | {:50} | {:50} | {}".format('#', 'Artist', 'Title','File Name'))
print('-'*160)
# Songs List
for i, mfile in enumerate(music_files):
    audiofile = eyed3.load(mfile)
    tag: eyed3.id3.tag.Tag = audiofile.tag
    print(f"{i:6} | {tag.artist:50} | {tag.title:50} | {mfile}")
