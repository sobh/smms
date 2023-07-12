#!/usr/bin/env python
#
# Description: Rename music file using slugified Artist, and Title.

# ---- Imports -----------------------------------------------------------------
# Batteries
import argparse
import sys

# Plugs
import eyed3

# Local
from utils import get_music_path, get_song_slug

# ---- Main --------------------------------------------------------------------
# ---- Command Line Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--dry-run', action='store_true'
                    , help="Don't rename any file, just show what would happen.")
args = parser.parse_args()

try:
    music_dir = get_music_path()
except FileNotFoundError:
    print("Unable to determine the 'Music Directory'.")
    sys.exit(-1)

# Go through all music files
music_files = list(music_dir.glob('**/*.mp3'))
for mfile in music_files:
    audiofile = eyed3.load(mfile)
    artist    = audiofile.tag.artist
    title     = audiofile.tag.title
    new_fname = mfile.with_stem(get_song_slug(artist, title))
    print(f"Renaming: {mfile.stem:60} -> {new_fname.stem:60}")
    if not args.dry_run:
        mfile.rename(new_fname)

