#!/usr/bin/env python
import argparse
import sys
from pathlib import Path
import shutil
import os
import sqlite3
import warnings
from typing import (List, Tuple)
import inquirer
from tqdm import tqdm

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", type=Path, help="directory the songs are outputed to, defualts to ~/Music")
    parser.add_argument("-a", "--all", action="store_true", help="extracts all songs instead of asking which ones to extract")
    global args
    args = parser.parse_args()

    osu_dir = get_osu_dir()
    if not os.path.isdir(osu_dir):
        raise FileNotFoundError("Cannot find osu!lazer directory")
    database = osu_dir / "client.db"
    
    songs = get_songs_from_database(database)

    music_dir = args.destination or Path.home() / "Music"
    
    for hash, name in tqdm(songs):
        file = osu_dir / "files" / hash[0] / hash [:2] / hash
        if not os.path.isfile(file):
            warnings.warn(f"Could not find song {name} at {file}! skipping...")
            continue
        
        try:
            shutil.copy2(file, music_dir / name)
        except FileNotFoundError or FileNotFoundError:
            warnings.warn(f"Failed to copy song {name}! Skipping...")
            continue
            
        # TODO Modify song metadata with mutagen, see https://stackoverflow.com/a/61343457/11779293
    
    print(f"Finished extracting {len(songs)} song{'' if len(songs) == 1 else 's'} to {music_dir}")


def get_songs_from_database(database: Path) -> List[Tuple[Path, str]]:

    # Connect to database in read-only mode
    connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    
    songs = []

    cursor = connection.execute("SELECT BeatmapSetInfoID, FileInfoID, Filename FROM BeatmapSetFileInfo;")
    for beatmap_set_info_id, file_info_id, filename in cursor.fetchall():
        # TODO use `beatmap_set_info_id` to filter non songs files
        hash = connection.execute(f"SELECT Hash FROM FileInfo WHERE ID='{file_info_id}'").fetchone()[0]
        songs.append((hash, filename))
    connection.close()

    if args.all:
        return songs

    questions = [
        inquirer.Checkbox("songs", message="What songs would you like to extract?", choices=[(song[1], song) for song in songs]),
    ]
    answers = inquirer.prompt(questions)
    return answers["songs"]

def get_osu_dir() -> Path:

    home = Path.home()

    if sys.platform == "linux":
        return home / ".local/share/osu"
    elif sys.platform == "win32":
        return home / "AppData/Roaming/osu"
    elif sys.platform == "darwin":
        return home / "Library/Application Support/osu"

if __name__ == "__main__":
    main()
