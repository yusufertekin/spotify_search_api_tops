import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from alotech.tracks.utils import (
    get_random_artist_by_genre,
    get_tracks_of_artist,
    find_top_tracks_of_artist,
    SpotifyException,
    GenreException,
)

logger = logging.getLogger(__name__)


def get_top_tracks_of_random_artist_by_genre(request, genre):
    try:
        artist = get_random_artist_by_genre(genre)
    except GenreException as e:
        return JsonResponse({"status": "false", "message": str(e)}, status=400)

    top_tracks = cache.get(artist)
    if not top_tracks:
        try:
            top_tracks = find_top_tracks_of_artist(
                get_tracks_of_artist(artist, settings.NUM_OF_TRACKS_TO_BE_FETCHED),
                settings.NUM_OF_TOP_TRACKS,
            )
            cache.set(artist, top_tracks, settings.TRACKS_CACHE_TIMEOUT)
        except SpotifyException as e:
            return JsonResponse({"status": "false", "message": str(e)}, status=500)

    return JsonResponse(top_tracks, safe=False)
