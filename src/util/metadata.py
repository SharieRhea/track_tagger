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

# IMPORTANT TODO: use a pydantic dataclass instead of dict for all the song info!!


# TODO: music-tag supports the following formats, add them: aac, aiff, dsf, flac, m4a, mp3, ogg, opus, wav, wv
def read_metadata(filepath: Path) -> dict:
    file = music_tag.load_file(filepath)
    assert isinstance(file, music_tag.id3.Mp3File)

    data = {}
    data["track_title"] = str(file["title"])
    data["artist"] = str(file["artist"])
    data["album_title"] = str(file["album"])
    data["album_artist"] = str(file["albumartist"])
    album_art = file["artwork"]

    if isinstance(album_art, music_tag.MetadataItem) and album_art.first is not None:
        album_art_bytes = album_art.first.data
        album_art = Image.open(BytesIO(album_art_bytes))
    else:
        album_art = None

    data["album_art"] = album_art

    data["tags"] = str(file["genre"]).split(", ")
    return data


def write_metadata(filepath: Path, data: dict) -> bool:
    try:
        file = music_tag.load_file(filepath)
        assert isinstance(file, music_tag.id3.Mp3File)
        file["title"] = data["track_title"]
        file["artist"] = data["artist"]
        file["album"] = data["album_title"]
        file["albumartist"] = data["album_artist"]

        # load the generic album cover by default, in case somehow there is no album cover data at all
        image_bytes = open("src/assets/generic_album_cover.jpg", "rb").read()

        if isinstance(data["album_art"], PngImageFile):
            bytes_io = BytesIO()
            data["album_art"].save(bytes_io, format="PNG")
            bytes_io.seek(0)
            image_bytes = bytes_io.read()
        elif isinstance(data["album_art"], JpegImageFile):
            bytes_io = BytesIO()
            data["album_art"].save(bytes_io, format="JPEG")
            bytes_io.seek(0)
            image_bytes = bytes_io.read()
        elif data["album_art"].src_base64 is not None and data["album_art"].src_base64 != "":
            image_bytes = base64.b64decode(data["album_art"].src_base64)
        elif data["album_art"].src != "":
            if "http" in data["album_art"].src:
                # this is an image url from last.fm, query to download the actual bytes in order to write
                result = query.get_album_image(data["album_art"].src)
                if result is not None:
                    image_bytes = result
            elif "generic_album_cover.jpg" not in data["album_art"].src:
                # this is a file that the user has locally
                image_bytes = open(data["album_art"].src, "rb").read()

        file["artwork"] = BytesIO(image_bytes).read()

        file["genre"] = ", ".join(data["tags"]).lower()
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
