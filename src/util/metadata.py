import base64
import logging
from io import BytesIO
from pathlib import Path

import music_tag
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from textual.logging import TextualHandler

from util import query

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)


# TODO: music-tag supports the following formats, add them: aac, aiff, dsf, flac, m4a, mp3, ogg, opus, wav, wv
def read_metadata(filepath: Path) -> tuple:
    file = music_tag.load_file(filepath)
    assert isinstance(file, music_tag.id3.Mp3File)

    title = str(file["title"])
    artist = str(file["artist"])
    album = str(file["album"])
    album_artist = str(file["albumartist"])
    album_art = file["artwork"]

    if isinstance(album_art, music_tag.MetadataItem) and album_art.first is not None:
        album_art_bytes = album_art.first.data
        album_art = Image.open(BytesIO(album_art_bytes))
    else:
        album_art = None

    tags = str(file["genre"]).split(", ")
    return (title, artist, album, album_artist, album_art, tags)


def write_metadata(filepath: Path, data: tuple) -> bool:
    try:
        file = music_tag.load_file(filepath)
        assert isinstance(file, music_tag.id3.Mp3File)
        file["title"] = data[0]
        file["artist"] = data[1]
        file["album"] = data[2]
        file["albumartist"] = data[3]

        # load the generic album cover by default, in case somehow there is no album cover data at all
        image_bytes = open("src/assets/generic_album_cover.jpg", "rb").read()

        if isinstance(data[4], PngImageFile):
            bytes_io = BytesIO()
            data[4].save(bytes_io, format="PNG")
            bytes_io.seek(0)
            image_bytes = bytes_io.read()
        elif isinstance(data[4], JpegImageFile):
            bytes_io = BytesIO()
            data[4].save(bytes_io, format="JPEG")
            bytes_io.seek(0)
            image_bytes = bytes_io.read()
        elif data[4].src_base64 is not None and data[4].src_base64 != "":
            image_bytes = base64.b64decode(data[4].src_base64)
        elif data[4].src != "":
            if "http" in data[4].src:
                # this is an image url from last.fm, query to download the actual bytes in order to write
                result = query.get_album_image(data[4].src)
                if result is not None:
                    image_bytes = result
            elif "generic_album_cover.jpg" not in data[4].src:
                # this is a file that the user has locally
                image_bytes = open(data[4].src, "rb").read()

        file["artwork"] = BytesIO(image_bytes).read()

        file["genre"] = ", ".join(data[5]).lower()
        file.save()
        return True
    except Exception as exception:
        logging.error("Error writing out file info: %s", exception)
        return False


def format_filename(
    format: str,
    title: str | None,
    artist: str | None,
    album_title: str | None,
    album_artist: str | None,
):
    # TODO: have an option for no spaces (probably replace with '_')
    if album_title is not None:
        format = format.replace("%at", album_title)
    if album_artist is not None:
        format = format.replace("%aa", album_artist)
    if title is not None:
        format = format.replace("%t", title)
    if artist is not None:
        format = format.replace("%a", artist)

    return format
