import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private playlist-read-collaborative"
))

df = pd.read_csv('tracks.csv')
track_ids = df['track_id'].unique().tolist()

print(f"Fetching audio features for {len(track_ids)} unique tracks...\n")

all_features = []

# Spotify allows max 100 tracks per request so we batch them
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i+100]
    features = sp.audio_features(batch)
    for f in features:
        if f:
            all_features.append({
                'track_id': f['id'],
                'energy': f['energy'],
                'valence': f['valence'],
                'danceability': f['danceability'],
                'tempo': f['tempo'],
                'acousticness': f['acousticness'],
                'instrumentalness': f['instrumentalness'],
                'loudness': f['loudness']
            })
    print(f"Fetched {min(i+100, len(track_ids))}/{len(track_ids)} tracks")

features_df = pd.DataFrame(all_features)
features_df.to_csv('audio_features.csv', index=False)
print(f"\nDone! Audio features saved to audio_features.csv")