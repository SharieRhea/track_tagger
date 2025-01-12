# track_tagger

track_tagger is a GUI program for editing metadata in mp3 files. Title, artist, album title, album artist, album cover, and genre are modified. The program uses the last.fm API to search for track information.

Please note that last.fm uses "tags" to describe the genre of a song. A song may have multiple tags, and are placed in the genre section of an mp3's metadata as a comma-separated list.

## Requirements

1. You will need a last.fm API key for making requests. Visit [this link](https://www.last.fm/api/account/create) to create an API account.
    1. Create a file called `.env` and provide your API key in the following format:
        ```
        KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```

## Installation

### From Source

### From Release

