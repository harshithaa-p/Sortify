import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private playlist-read-collaborative"
))

user = sp.current_user()
print(f"\nLogged in as: {user['display_name']}\n")

playlists = sp.current_user_playlists()

print("Your playlists:")
print("-" * 40)

for i, playlist in enumerate(playlists['items']):
    try:
        playlist_details = sp.playlist(playlist['id'])
        track_count = playlist_details['items']['total']
    except:
        track_count = '?'
    print(f"{i+1}. {playlist['name']} - {track_count} songs")