import logging
from typing import List

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
    results = info.json()

    if not results or "track" not in results:
        return None

    data = {}
    data["track_title"] = results["track"]["name"]
    data["artist"] = results["track"]["artist"]["name"]
    data["album_title"] = results["track"]["album"]["title"]
    data["album_artist"] = results["track"]["album"]["artist"]
    # TODO: handle when there is no valid image list
    data["album_art"] = results["track"]["album"]["image"][-1]["#text"]
    tags: List[str] = []
    for tag in results["track"]["toptags"]["tag"]:
        tags.append(tag["name"].lower())
    data["tags"] = tags

    return data


def get_album_image(url) -> bytes | None:
    info = requests.get(url)
    if info.status_code != 200:
        return None
    # FIX: sanitize this and make sure it's an image
    return info.content
