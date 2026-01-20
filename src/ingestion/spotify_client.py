import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client() -> spotipy.Spotify:
    load_dotenv()

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    cache_path = os.getenv("SPOTIPY_CACHE_PATH", ".cache-spotify")

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError(
            "Missing Spotify env vars. Ensure SPOTIPY_CLIENT_ID, "
            "SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI are set in .env"
        )

    scope = "user-library-read"

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=cache_path,
        open_browser=True,
    )
    return spotipy.Spotify(auth_manager=auth_manager)
