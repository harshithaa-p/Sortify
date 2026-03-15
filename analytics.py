import pandas as pd

df = pd.read_csv('tracks.csv')

print("=== SORTIFY ANALYTICS ===\n")

# Total stats
print(f"Total tracks: {len(df)}")
print(f"Unique tracks: {df['track_id'].nunique()}")
print(f"Unique artists: {df['artist'].nunique()}")
print(f"Total playlists: {df['playlist'].nunique()}\n")

# Top 10 most repeated songs across playlists
print("=== SONGS IN MULTIPLE PLAYLISTS ===")
repeated = df.groupby(['track_id', 'track_name', 'artist'])['playlist'].count().reset_index()
repeated.columns = ['track_id', 'track_name', 'artist', 'playlist_count']
repeated = repeated[repeated['playlist_count'] > 1].sort_values('playlist_count', ascending=False)
print(repeated[['track_name', 'artist', 'playlist_count']].head(10).to_string(index=False))

print("\n=== TOP 10 ARTISTS ===")
top_artists = df.groupby('artist')['track_id'].count().sort_values(ascending=False).head(10)
for artist, count in top_artists.items():
    print(f"{artist} - {count} songs")

print("\n=== SONGS PER PLAYLIST ===")
playlist_counts = df.groupby('playlist')['track_id'].count().sort_values(ascending=False)
for playlist, count in playlist_counts.items():
    print(f"{playlist} - {count} songs")