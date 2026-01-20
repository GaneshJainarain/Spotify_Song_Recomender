import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    # Load .env from the same folder as this script
    env_path = Path(__file__).resolve().parents[2] / ".env"
    loaded = load_dotenv(env_path)


    print("dotenv loaded:", loaded)
    print("SPOTIPY_CLIENT_ID present:", bool(os.getenv("SPOTIPY_CLIENT_ID")))
    print("SPOTIPY_REDIRECT_URI:", os.getenv("SPOTIPY_REDIRECT_URI"))

    scope = "user-read-private user-library-read"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope,
            cache_path=os.getenv("SPOTIPY_CACHE_PATH", ".cache-spotify"),
            open_browser=True,
        )
    )

    me = sp.current_user()
    print("✅ Connected as:", me.get("display_name"), "| country:", me.get("country"))

    liked = sp.current_user_saved_tracks(limit=5)
    print("\n🎵 First 5 liked tracks:")
    for i, item in enumerate(liked.get("items", []), 1):
        t = item["track"]
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"{i}. {t['name']} — {artists}")

if __name__ == "__main__":
    main()
