from django.urls import path

from . import views


app_name = "tracks"

urlpatterns = [
    path("<slug:genre>/", views.get_top_tracks_of_random_artist_by_genre, name="by-genre"),
]
