import streamlit as st
import pandas as pd
from auth import get_spotify_client, login_button

st.set_page_config(page_title="Sortify", page_icon="🎵", layout="wide")

st.title("🎵 Sortify")
st.caption("Your personal Spotify analytics dashboard")

sp = get_spotify_client()

if sp is None:
    st.markdown("### Welcome to Sortify!")
    st.write("Analyse your Spotify playlists — find repeated songs, top artists, compare playlists and more.")
    st.write("")
    login_button()
    st.stop()

# Logout button
if st.sidebar.button("Logout"):
    del st.session_state['token_info']
    st.rerun()

user = sp.current_user()
st.sidebar.write(f"Logged in as **{user['display_name']}**")

@st.cache_data(ttl=3600)
def load_data(user_id):
    playlists_data = []
    results = sp.current_user_playlists()
    for playlist in results['items']:
        playlists_data.append({
            'id': playlist['id'],
            'name': playlist['name']
        })

    all_tracks = []
    progress = st.progress(0)
    total = len(playlists_data)
    
    for idx, playlist in enumerate(playlists_data):
        try:
            results = sp.playlist_items(playlist['id'])
            while results:
                for item in results['items']:
                    track = item.get('track') or item.get('item')
                    if track and track.get('id'):
                        all_tracks.append({
                            'playlist': playlist['name'],
                            'track_id': track['id'],
                            'track_name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'album': track['album']['name'],
                            'duration_ms': track.get('duration_ms', 0),
                            'release_date': track['album'].get('release_date', 'unknown')
                        })
                results = sp.next(results) if results['next'] else None
        except:
            pass
        progress.progress((idx + 1) / total)

    return pd.DataFrame(all_tracks)
with st.spinner("🎵 Fetching your playlists for the first time... this takes 1-2 minutes but won't happen again!"):
    df = load_data(user['id'])

if df.empty:
    st.error("No tracks found!")
    st.stop()

# Top stats
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tracks", len(df))
col2.metric("Unique Tracks", df['track_id'].nunique())
col3.metric("Unique Artists", df['artist'].nunique())
col4.metric("Playlists", df['playlist'].nunique())

st.divider()

# Top artists
st.subheader("🎤 Top 10 Artists")
top_artists = df.groupby('artist')['track_id'].count().sort_values(ascending=False).head(10).reset_index()
top_artists.columns = ['Artist', 'Songs']
st.bar_chart(top_artists.set_index('Artist'))

st.divider()

# Songs in multiple playlists
st.subheader("🔁 Songs Across Multiple Playlists")
repeated = df.groupby(['track_id', 'track_name', 'artist'])['playlist'].count().reset_index()
repeated.columns = ['track_id', 'Track', 'Artist', 'Playlists']
repeated = repeated[repeated['Playlists'] > 1].sort_values('Playlists', ascending=False)
st.dataframe(repeated[['Track', 'Artist', 'Playlists']], width='stretch')

st.divider()

# Songs per playlist
st.subheader("📂 Songs per Playlist")
playlist_counts = df.groupby('playlist')['track_id'].count().sort_values(ascending=False).reset_index()
playlist_counts.columns = ['Playlist', 'Songs']
st.bar_chart(playlist_counts.set_index('Playlist'))

st.divider()

# Explore a playlist
st.subheader("🔍 Explore a Playlist")
selected = st.selectbox("Choose a playlist", df['playlist'].unique())
playlist_df = df[df['playlist'] == selected].copy()
playlist_df['duration'] = (playlist_df['duration_ms'] / 60000).round(2)

artists = ['All'] + sorted(playlist_df['artist'].dropna().unique().tolist())
selected_artist = st.selectbox("Filter by artist", artists)
if selected_artist != 'All':
    playlist_df = playlist_df[playlist_df['artist'] == selected_artist]

sort_by = st.selectbox("Sort by", ['track_name', 'artist', 'duration', 'release_date'])
sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)
playlist_df = playlist_df.sort_values(sort_by, ascending=(sort_order == 'Ascending'))

st.dataframe(
    playlist_df[['track_name', 'artist', 'album', 'duration', 'release_date']].rename(columns={
        'track_name': 'Track',
        'artist': 'Artist',
        'album': 'Album',
        'duration': 'Duration (min)',
        'release_date': 'Release Date'
    }),
    width='stretch'
)

st.divider()

# Search
st.subheader("🔎 Search Across All Playlists")
search = st.text_input("Search by song or artist name")
if search:
    results = df[
        df['track_name'].str.contains(search, case=False, na=False) |
        df['artist'].str.contains(search, case=False, na=False)
    ][['track_name', 'artist', 'playlist']].rename(columns={
        'track_name': 'Track',
        'artist': 'Artist',
        'playlist': 'Playlist'
    })
    st.write(f"Found {len(results)} results")
    st.dataframe(results, width='stretch')

st.divider()

# Compare playlists
st.subheader("⚖️ Compare Two Playlists")
col1, col2 = st.columns(2)
playlist_a = col1.selectbox("Playlist A", df['playlist'].unique(), key="a")
playlist_b = col2.selectbox("Playlist B", df['playlist'].unique(), key="b")

if playlist_a != playlist_b:
    tracks_a = set(df[df['playlist'] == playlist_a]['track_id'])
    tracks_b = set(df[df['playlist'] == playlist_b]['track_id'])

    common = tracks_a & tracks_b
    only_a = tracks_a - tracks_b
    only_b = tracks_b - tracks_a

    col1, col2, col3 = st.columns(3)
    col1.metric(f"Only in {playlist_a}", len(only_a))
    col2.metric("In Both", len(common))
    col3.metric(f"Only in {playlist_b}", len(only_b))

    if common:
        st.write("**Songs in both playlists:**")
        common_df = df[df['track_id'].isin(common)][['track_name', 'artist']].drop_duplicates()
        common_df.columns = ['Track', 'Artist']
        st.dataframe(common_df, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Only in {playlist_a}:**")
        only_a_df = df[df['track_id'].isin(only_a)][['track_name', 'artist']].drop_duplicates()
        only_a_df.columns = ['Track', 'Artist']
        st.dataframe(only_a_df, width='stretch')
    with col2:
        st.write(f"**Only in {playlist_b}:**")
        only_b_df = df[df['track_id'].isin(only_b)][['track_name', 'artist']].drop_duplicates()
        only_b_df.columns = ['Track', 'Artist']
        st.dataframe(only_b_df, width='stretch')
else:
    st.warning("Please select two different playlists!")