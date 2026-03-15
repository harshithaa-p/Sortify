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

def get_all_playlists():
    playlists = []
    results = sp.current_user_playlists()
    for playlist in results['items']:
        playlists.append({
            'id': playlist['id'],
            'name': playlist['name']
        })
    return playlists

def get_playlist_tracks(playlist_id, playlist_name):
    tracks = []
    results = sp.playlist_items(playlist_id)
    
    while results:
        for item in results['items']:
            track = item.get('track') or item.get('item')
            if track and track.get('id'):
                tracks.append({
                    'playlist': playlist_name,
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration_ms': track.get('duration_ms', 0),
                    'release_date': track['album'].get('release_date', 'unknown'),
                    'popularity': 0
                })
        results = sp.next(results) if results['next'] else None

    # Fetch popularity in batches of 50
    for i in range(0, len(tracks), 50):
        batch = tracks[i:i+50]
        ids = [t['track_id'] for t in batch]
        try:
            full_tracks = sp.tracks(ids)['tracks']
            for j, full in enumerate(full_tracks):
                if full:
                    tracks[i+j]['popularity'] = full.get('popularity', 0)
        except:
            pass

    return tracks

all_tracks = []
playlists = get_all_playlists()

print("Fetching tracks from your playlists...\n")

for playlist in playlists:
    print(f"Fetching: {playlist['name']}")
    try:
        tracks = get_playlist_tracks(playlist['id'], playlist['name'])
        all_tracks.extend(tracks)
    except Exception as e:
        print(f"  Skipped (no access)")
if all_tracks:
    df = pd.DataFrame(all_tracks)
    df.to_csv('tracks.csv', index=False)
    print(f"\nDone! {len(df)} total tracks saved to tracks.csv")
    print(f"Across {df['playlist'].nunique()} playlists")
else:
    print("\nNo tracks fetched!")

