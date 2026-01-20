
# SpotifyML
A machine learning–ready pipeline for analyzing Spotify liked songs

## Overview

SpotifyML is a data ingestion and analysis project that uses the Spotify Web API to collect a user’s liked songs and enrich them with audio feature metadata such as danceability, energy, tempo, and valence.

The project is designed to produce clean, structured datasets suitable for music analysis, clustering, recommendation systems, and machine learning experimentation, while following real-world data engineering and ML best practices.

---

## Features

- Fetches liked songs from the Spotify API
- Enriches tracks with audio feature metadata
- Stores raw data in Parquet format for efficient processing
- Notebook-based exploration for fast iteration
- Modular Python package structure
- Secure API access using environment variables

---

## Project Structure

SpotifyML/
├── configs/
│   └── config.yaml
│
├── data/
│   └── raw/
│       └── liked_songs.parquet
│
├── notebooks/
│   └── main.ipynb
│
├── src/
│   ├── ingestion/
│   │   ├── spotify_client.py
│   │   ├── pull_liked_snapshot.py
│   │   └── test_spotify.py
│   │
│   └── __init__.py
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

---

## Data Collected

### Track Metadata
- Track name
- Artist(s)
- Album
- Release date
- Explicit flag
- Popularity
- Spotify track ID

### Audio Features
- Danceability
- Energy
- Tempo (BPM)
- Valence

Example extracted dataset:

    audio_df[["track_id", "danceability", "energy", "tempo", "valence"]]

---

## Setup Instructions

### 1. Clone the repository

    git clone https://github.com/your-username/SpotifyML.git
    cd SpotifyML

### 2. Create and activate a virtual environment

    python -m venv venv
    source venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Configure Spotify API credentials

Create a .env file:

    SPOTIFY_CLIENT_ID=your_client_id
    SPOTIFY_CLIENT_SECRET=your_client_secret
    SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

Spotify credentials can be obtained from the Spotify Developer Dashboard.

---

## Running the Project

### Pull liked songs from Spotify

    python main.py

This will authenticate with Spotify, pull liked tracks, and store them in:

    data/raw/liked_songs.parquet

### Explore the data

Open the notebook:

    notebooks/main.ipynb

From there you can inspect distributions, engineer features, cluster songs, and build ML models.

---

## Example Use Cases

- Personal music taste profiling
- Feature distribution analysis
- Song clustering
- Recommendation system prototyping
- Machine learning experimentation

---

## Future Enhancements

- Artist and genre-level aggregation
- Song clustering by mood or energy
- Recommendation engine
- MLflow experiment tracking
- DVC for dataset versioning
- FastAPI service for live recommendations
- Dashboard interface

---

## License

MIT License

---

## Author

Ganesh Jainarain  
AI Researcher / Machine Learning Engineer
