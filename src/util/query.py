import logging

import requests

ENDPOINT = "https://ws.audioscrobbler.com/2.0/"


def album_search(key, album) -> dict | None:
    parameters = {
        "method": "album.search",
        "api_key": key,
        "album": album,
        "format": "json",
    }
    info = requests.get(ENDPOINT, params=parameters)
    if info.status_code != 200:
        return None

    logging.info(info.json())
    return info.json()


def track_getinfo(key, title, artist) -> dict | None:
    parameters = {
        "method": "track.getInfo",
        "api_key": key,
        "track": title,
        "artist": artist,
        "format": "json",
    }
    info = requests.get(ENDPOINT, params=parameters)
    if info.status_code != 200:
        return None
    logging.info(info.json())
    _ = info.json()

    # TODO: validate and turn into tuple

    return info.json()


def get_album_image(url) -> bytes | None:
    info = requests.get(url)
    if info.status_code != 200:
        return None
    return info.content
