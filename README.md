# track_tagger

track_tagger is a GUI program built with [flet](https://github.com/flet-dev/flet) for editing metadata in mp3 files. Title, artist, album title, album artist, album cover, and genre are modified. The user may optionally provide a [last.fm](https://www.last.fm) API key to search for track information.

Please note that track_tagger follows the last.fm convention of using "tags" to describe the genre of a song. A song may have multiple tags, and are they are placed in the genre section of an mp3's metadata as a comma-separated list.

## Installation

### From Release

Download the latest release [here](https://github.com/SharieRhea/TrackTagger/releases)!
Right now, only a linux build is available.

#### Application Launcher

To add track_tagger to your list of applications on Ubuntu distributions:

1. Create a `track_tagger.desktop` file in `~/.local/share/applications/`
2. Add the following contents to the file:
    * *If you do not want to use the default system icon, download `icon.png` from `/src/assets` and provide its path to the `Icon` field. Otherwise, omit the `Icon=` line*
    ```
    [Desktop Entry]
    Name=track_tagger
    Exec=/path/to/downloaded/exec/track_tagger
    Type=Application
    Icon=/optional/path/to/icon.png
    StartupNotify=true
    StartupWMClass=track_tagger
    ```

### From Source

#### Dependencies

* [python3](https://www.python.org/downloads/)

#### Steps

1. Clone the repository
2. Create virtual environment: `python3 -m venv .venv`
3. Activate the venv: `source .venv/bin/activate`
4. Install flet: `pip install flet`
5. Run the app: `flet run`

## Development

track_tagger is under development, *please* submit issues for any bugs you find or ideas you have!
