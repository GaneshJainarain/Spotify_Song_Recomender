from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from dotenv import find_dotenv, load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm


@dataclass
class LikedSongsConfig:
    max_tracks: int = 2000            # increase later
    market: str = "US"                # affects availability for some tracks
    save_path: Optional[Path] = None  # e.g. Path("data/raw/liked_songs.parquet")


def load_env() -> None:
    """
    Loads .env from repo root. Works even if you run from subfolders.
    """
    env_path = find_dotenv(".env", usecwd=True)
    if env_path:
        load_dotenv(env_path)
        return
    # fallback: repo_root/src/ingestion/liked_songs.py -> repo_root/.env
    fallback = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(fallback)


def get_spotify_client() -> spotipy.Spotify:
    """
    Creates an authenticated Spotify client using Spotipy OAuth.
    Requires env vars in .env:
      SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
    """
    scope = "user-library-read user-read-private"

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    cache_path = os.getenv("SPOTIPY_CACHE_PATH", ".cache-spotify")

    if not client_id or not client_secret or not redirect_uri:
        raise ValueError(
            "Missing Spotify env vars. Ensure SPOTIPY_CLIENT_ID, "
            "SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI are set in .env"
        )

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=cache_path,
            open_browser=True,
        )
    )


def fetch_liked_songs(
    sp: spotipy.Spotify,
    max_tracks: int = 2000,
    market: str = "US",
) -> List[Dict[str, Any]]:
    """
    Fetches up to max_tracks from the user's 'Liked Songs' library.
    Returns the raw Spotify API items.
    """
    items: List[Dict[str, Any]] = []
    limit = 50
    offset = 0

    with tqdm(total=max_tracks, desc="Fetching liked songs") as pbar:
        while len(items) < max_tracks:
            resp = sp.current_user_saved_tracks(limit=limit, offset=offset, market=market)
            batch = resp.get("items", [])
            if not batch:
                break

            items.extend(batch)
            offset += len(batch)
            pbar.update(len(batch))

            if resp.get("next") is None:
                break

    return items[:max_tracks]


def liked_songs_to_df(items: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts Spotify liked track items into a flat dataframe suitable for storage/ML.
    """
    snapshot_utc = datetime.now(timezone.utc).isoformat()
    rows = []

    for it in items:
        track = it.get("track") or {}
        if not track:
            continue

        tid = track.get("id")
        if not tid:
            continue

        artists = track.get("artists") or []
        artist_names = "|".join([a.get("name") for a in artists if a.get("name")])
        artist_ids = "|".join([a.get("id") for a in artists if a.get("id")])

        album = track.get("album") or {}

        rows.append(
            {
                "snapshot_utc": snapshot_utc,
                "added_at": it.get("added_at"),
                "track_id": tid,
                "track_name": track.get("name"),
                "explicit": track.get("explicit"),
                "popularity": track.get("popularity"),
                "duration_ms": track.get("duration_ms"),
                "artist_names": artist_names,
                "artist_ids": artist_ids,
                "album_id": album.get("id"),
                "album_name": album.get("name"),
                "release_date": album.get("release_date"),
                "release_date_precision": album.get("release_date_precision"),
            }
        )

    return pd.DataFrame(rows)


def get_liked_songs_df(cfg: LikedSongsConfig = LikedSongsConfig()) -> pd.DataFrame:
    """
    High-level convenience function:
      - loads env
      - auths Spotify
      - fetches liked songs
      - converts to dataframe
      - optionally saves to cfg.save_path
    """
    load_env()
    sp = get_spotify_client()

    items = fetch_liked_songs(sp, max_tracks=cfg.max_tracks, market=cfg.market)
    df = liked_songs_to_df(items)

    if cfg.save_path is not None:
        cfg.save_path.parent.mkdir(parents=True, exist_ok=True)
        if cfg.save_path.suffix.lower() == ".csv":
            df.to_csv(cfg.save_path, index=False)
        else:
            # default parquet
            df.to_parquet(cfg.save_path, index=False)

    return df


if __name__ == "__main__":
    # Example run:
    cfg = LikedSongsConfig(max_tracks=1000, save_path=Path("data/raw/liked_songs.parquet"))
    df = get_liked_songs_df(cfg)
    print(df.head(5))
    print("\nRows:", len(df))
