# osume - Osu! Music Extractor

Extract music from osu!lazer beatmaps

AUR package coming soon

## Usage

Note: The script has only been tested on Linux, but should work on Windows and MacOS as well

Get the latest version of [python](https://www.python.org/downloads/)

```
git clone https://github.com/bbb651/osume/
cd osume
pip install -r requirements.txt
python osume.py
```

### Arguments
- `-d`, `--destination` - directory the songs are outputed to, defaults to `~/Music`
- `-a`, `--all` - extracts all songs of asking which ones to extract

## Known Issues
- All files are extracted not just songs, and 
- Songs with directories in their name will fail to extract
- Not all songs have proper metadata
