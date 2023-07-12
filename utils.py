# ---- Imports -----------------------------------------------------------------
# Batteries
from pathlib import Path
import subprocess
import re

# Plugs
from slugify import slugify

# ---- Functions ---------------------------------------------------------------
def get_music_path():
    dirs = []
    # XDG User Music Directory
    try:
        out = subprocess.run(['xdg-user-dir', 'MUSIC'], stdout=subprocess.PIPE).stdout
        xdg_music_dir = out.decode().split('\n')[0]
        dirs.append(Path(xdg_music_dir))
    except:
        pass
    # Default Directories
    dirs.extend([
            Path('Music').expanduser(),
            Path('music').expanduser(),
        ])

    for dir in dirs:
        if dir.is_dir():
            return dir
    else:
        raise FileNotFoundError("Unable to locate the user's Music Directory")

def get_song_slug(artist, title):
    pattern = r'\s*(feat|\&).*'
    replacements = (("'",''), ('.',''))     # Remove quotes, and dots entirly
    artist_clean = re.sub(pattern, '', artist, flags=re.IGNORECASE)
    artist_slug = slugify(artist_clean, separator='_', replacements=replacements)
    title_clean = re.sub(pattern, '', title, flags=re.IGNORECASE)
    title_slug = slugify(title_clean, separator='_', replacements=replacements)
    return artist_slug + '-' + title_slug
