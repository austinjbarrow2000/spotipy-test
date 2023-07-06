import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json

load_dotenv()

scope = "playlist-read-private"  # Adjust the scope based on your needs
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=client_redirect_uri,
        scope=scope,
    )
)


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    return tracks


def get_song_info(song):
    song_info = {}
    track = song["track"]
    song_info["name"] = track["name"]
    song_info["artists"] = [artist["name"] for artist in track["artists"]]
    song_info["album"] = track["album"]["name"]
    song_info["release_date"] = track["album"]["release_date"]
    song_info["popularity"] = track["popularity"]
    song_info["duration_ms"] = track["duration_ms"]
    song_info["external_urls"] = track["external_urls"]

    audio_features = sp.audio_features(track["id"])[0]
    song_info["acousticness"] = audio_features["acousticness"]
    song_info["danceability"] = audio_features["danceability"]
    song_info["energy"] = audio_features["energy"]
    song_info["instrumentalness"] = audio_features["instrumentalness"]
    song_info["liveness"] = audio_features["liveness"]
    song_info["loudness"] = audio_features["loudness"]
    song_info["speechiness"] = audio_features["speechiness"]
    song_info["tempo"] = audio_features["tempo"]
    song_info["time_signature"] = audio_features["time_signature"]
    song_info["valence"] = audio_features["valence"]
    song_info["key"] = audio_features["key"]
    song_info["mode"] = audio_features["mode"]

    return song_info


playlist_id = "5D0Zr6FQmn4BYnpIykmUYb"  # Replace with the playlist ID

playlist_tracks = get_playlist_tracks(playlist_id)

for song in playlist_tracks:
    song_info = get_song_info(song)
    print(json.dumps(song_info, indent=4))
