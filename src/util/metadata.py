from types import NoneType
import music_tag
import base64
from io import BytesIO

# TODO: figure out how to make pyright happy

def read_metadata(filepath: str) -> tuple:
    file = music_tag.load_file(filepath)
    title = str(file["title"])
    artist = str(file["artist"])
    album = str(file["album"])
    album_artist = str(file["albumartist"])
    album_art = file["artwork"]
    if album_art.first is not None:
        album_art_bytes = album_art.first.data
        # encode into base64 then get the base64 string for displaying with flet image
        base64_bytes = base64.b64encode(album_art_bytes)
        album_art = base64_bytes.decode("ascii")

    tags = str(file["genre"]).split(", ")

    return (title, artist, album, album_artist, album_art, tags)

def write_metadata(filepath: str, data: tuple):
    file = music_tag.load_file(filepath)
    file["title"] = data[0]
    file["artist"] = data[1]
    file["album"] = data[2]
    file["albumartist"] = data[3] 
    file["artwork"] = BytesIO(data[4]).read()
    file["genre"] = ", ".join(data[5])
    file.save()
