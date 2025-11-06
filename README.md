# track_tagger

track_tagger is a terminal user interface (TUI) program built with [textual](https://textual.textualize.io/) for editing metadata in music files. Title, artist, album title, album artist, album cover, and genre are modified. The user may optionally provide a [last.fm](https://www.last.fm) API key to search for track information.

Please note that track_tagger follows the last.fm convention of using "tags" to describe the genre of a song. A song may have multiple tags, and are they are placed in the genre section of the metadata as a comma-separated list.

## Installation

#### Dependencies

* [python3](https://www.python.org/downloads/)
* [textual](https://pypi.org/project/textual/)
* [music-tag](https://pypi.org/project/music-tag/)
* [requests](https://pypi.org/project/requests/)

#### Steps

1. Clone the repository
2. Create virtual environment: `python3 -m venv .venv`
3. Activate the venv: `source .venv/bin/activate`
4. Install pip dependencies: 
    1. `pip install textual`
    2. `pip install music-tag`
    3. `pip install requests`
5. Run the app: `textual run main.py`

## Development

track_tagger is under development, *please* submit issues for any bugs you find or ideas you have!

### Roadmap

1. Basic Functionality

- [ ] select a directory or file(s)
- [x] read existing metadata from a file
- [ ] write new metadata to a file
    - [ ] handling multiple image sources (last.fm, local file)
- [ ] search last.fm for a track's info based on title and artist
- [x] persistent settings (API key, file name format, locked tags)
- [ ] list of session files next to edit page
- [ ] add logging!

2. Features

- [ ] search alternative album covers
- [ ] bulk edit album covers
- [ ] ability to toggle tag behavior
    - default: selecting a tag (provided by last.fm) saves for the current session only
    - persistent: selecting a tag (provided by last.fm) saves in persistent configuration
