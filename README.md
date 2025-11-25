# track_tagger

track_tagger is a terminal user interface (TUI) program built with [textual](https://textual.textualize.io/) for editing metadata in music files. Title, artist, album title, album artist, album cover, and genre are modified. The user may optionally provide a [last.fm](https://www.last.fm) API key to search for track information.

Please note that track_tagger follows the last.fm convention of using "tags" to describe the genre of a song. A song may have multiple tags, and are they are placed in the genre section of the metadata as a comma-separated list.

## Installation

### A Note on Fonts

track_tagger is a TUI program, which means that all UI is rendered in the the terminal. This means you will need a terminal emulator with a *monospaced* font. Additionally, the textual library uses Unicode emojis for certain icons (directories and files). If your chosen font does not have Unicode glyphs (and many nerd fonts do not!), ensure you have a fallback font.

Personally, I use [JetBrainsMonoNL Mono](https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip) and [Noto Color Emoji](https://fonts.google.com/noto/specimen/Noto+Color+Emoji).

### From Source

#### Dependencies

* [python3](https://www.python.org/downloads/)
* [textual](https://pypi.org/project/textual/) for the TUI
* [music-tag](https://pypi.org/project/music-tag/) for reading/writing metadata
* [requests](https://pypi.org/project/requests/) for querying the last.fm API
* [rich-pixels](https://github.com/darrenburns/rich-pixels) for displaying album art
* [pyyaml](https://pypi.org/project/PyYAML/) for parsing configuration files

#### Steps

1. Clone the repository
2. Create a virtual environment (optional): `python3 -m venv .venv`
3. Activate the venv (optional): `source .venv/bin/activate`
4. Install pip dependencies: 
    1. `pip install textual`
    2. `pip install music-tag`
    3. `pip install requests`
    4. `pip install rich-pixels`
    5. `pip install pyyaml`
5. Run the app: `python src/main.py`

#### Developers

For development, the `textual-dev` package may be useful. Install with `pip install textual-dev`.

* Use `textual console` to start the console. **Exclude** logging messages with `-x {NAME}`. The options are:
    * EVENT
    * DEBUG
    * INFO
    * WARNING
    * ERROR
    * PRINT
    * SYSTEM
    * LOGGING
* Run the app in development mode using `textual run main.py -dev`. This will connect to a running console and also **apply live edits from CSS files**.

## Development

track_tagger is under development, *please* submit issues for any bugs you find or ideas you have!

### Roadmap

1. Basic Functionality

- [x] select a directory or file(s)
- [x] read existing metadata from a file
- [x] write new metadata to a file
    - [x] handling multiple image sources (last.fm, local file)
- [x] search last.fm for a track's info based on title and artist
- [x] persistent settings (API key, file name format, locked tags)
- [x] list of session files next to edit page
- [ ] add logging!
- [ ] add tests!

2. Features

- [ ] search alternative album covers
- [ ] bulk edit album covers
- [ ] ability to toggle tag behavior
    - default: selecting a tag (provided by last.fm) saves for the current session only
    - persistent: selecting a tag (provided by last.fm) saves in persistent configuration
- [ ] support for other sites? (discogs, beets.io, pandora)
