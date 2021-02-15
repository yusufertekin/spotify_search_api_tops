import json

from base64 import b64encode
from random import randint
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import logging

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class SpotifyException(Exception):
    pass


class GenreException(Exception):
    pass


def get_random_artist_by_genre(genre):
    artist_list = cache.get(genre)
    if artist_list:
        return artist_list[randint(0, len(artist_list) - 1)]
    else:
        error_message = f"Genre not found: {genre}"
        logger.error(error_message)
        raise GenreException(error_message)


def make_request(req):
    try:
        return urlopen(req)
    except HTTPError as e:
        error_message = f"The server couldn't fulfill the request. Error code: {e.code}"
        logger.error(error_message)
        raise SpotifyException(error_message)
    except URLError as e:
        error_message = f"We failed to reach a server. Reason: {e.reason}"
        logger.error(error_message)
        raise SpotifyException(error_message)


def get_access_token():
    """Makes a request to get access token to be used to authenticate on Spotify API"""
    data = urlencode({"grant_type": "client_credentials"}).encode()
    req = Request(f"{settings.SPOTIFY_ACCOUNT_ENDPOINT}", data=data)
    encoded_auth = (
        f"{settings.SPOTIFY_API_CLIENT_ID}:{settings.SPOTIFY_API_CLIENT_SECRET}"
    ).encode()
    req.add_header("Authorization", f"Basic {b64encode(encoded_auth).decode()}")
    logger.info("Making request to get access token for Spotify API")
    resp = make_request(req)
    return json.loads(resp.read().decode())["access_token"]


def get_tracks_of_artist(artist, num_of_tracks):
    """Makes requests to Spotify Search API until successfully find num_of_tracks many tracks.
    Parses desired info out of dataset.
    """
    offset = 0
    tracks = []
    limit = 50
    while len(tracks) < num_of_tracks:
        params = urlencode(
            {
                "q": f'artist:"{artist.upper()}"',
                "type": "track",
                "offset": offset,
                "limit": limit,
            }
        )
        access_token = get_access_token()
        req = Request(f"{settings.SPOTIFY_SEARCH_API_BASE_URL}?{params}")
        req.add_header("Authorization", f"Bearer {access_token}")
        logger.info(f"Making request to get tracks for {artist}[{offset}:{limit}]")
        resp = make_request(req)
        for track in json.loads(resp.read().decode())["tracks"]["items"]:
            if len(tracks) == num_of_tracks:
                break

            if track["artists"][0]["name"].upper() == artist.upper():
                tracks.append(
                    {
                        "artist": artist,
                        "track": track["name"],
                        "album_image_url": track["album"]["images"][0]["url"],
                        "preview_url": track["preview_url"],
                        "popularity": track["popularity"],
                    }
                )

        offset += limit
    return tracks


def find_top_tracks_of_artist(tracks, num_of_top_tracks):
    """Sorts tracks by popularity, returns number of top tracks without popularity info"""
    return [
        {k: v for k, v in track.items() if k != "popularity"}
        for track in sorted(
            tracks, key=lambda track: (track["popularity"], track["track"])
        )[:num_of_top_tracks]
    ]
