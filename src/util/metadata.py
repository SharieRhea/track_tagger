from io import BytesIO
import music_tag
import base64

from util import query

def read_metadata(filepath: str) -> tuple:
    file = music_tag.load_file(filepath)
    assert isinstance(file, music_tag.id3.Mp3File)

    title = str(file["title"])
    artist = str(file["artist"])
    album = str(file["album"])
    album_artist = str(file["albumartist"])
    album_art = file["artwork"]

    if isinstance(album_art, music_tag.MetadataItem) and album_art.first is not None:
        album_art_bytes = album_art.first.data
        # encode into base64 then get the base64 string for displaying with flet image
        base64_bytes = base64.b64encode(album_art_bytes)
        album_art = base64_bytes.decode("ascii")
    else:
        album_art = None

    tags = str(file["genre"]).split(", ")

    return (title, artist, album, album_artist, album_art, tags)

def write_metadata(filepath: str, data: tuple):
    file = music_tag.load_file(filepath)
    assert isinstance(file, music_tag.id3.Mp3File)
    file["title"] = data[0]
    file["artist"] = data[1]
    file["album"] = data[2]
    file["albumartist"] = data[3] 

    # load the generic album cover by default, in case somehow there is no album cover data at all
    image_bytes = open("src/assets/generic_album_cover.jpg", "rb").read()

    if data[4].src_base64 is not None and data[4].src_base64 is not "":
        image_bytes = base64.b64decode(data[4].src_base64)
    elif data[4].src is not "":
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

def format_filename(format: str, title: str | None, artist: str | None, album_title: str | None, album_artist: str | None):
    if album_title is not None:
        format = format.replace("%at", album_title)
    if album_artist is not None:
        format = format.replace("%aa", album_artist)
    if title is not None:
        format = format.replace("%t", title)
    if artist is not None:
        format = format.replace("%a", artist)

    return format
