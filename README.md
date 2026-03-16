# 🎵 Sortify

A personal Spotify analytics dashboard that lets you deep-dive into your playlists — find repeated songs, compare playlists, discover your top artists and more.

🔗 **Live App:** https://sortify-hjp3fgyncbyvodhufxyx8w.streamlit.app/

---

## Features

- **Spotify OAuth Login** — securely log in with your own Spotify account
- **Library Overview** — see your total tracks, unique songs, artists and playlists at a glance
- **Top Artists** — bar chart of your most listened to artists
- **Repeated Songs** — find songs that appear across multiple playlists
- **Playlist Explorer** — browse any playlist with sort and filter by artist, duration and release date
- **Search** — search any song or artist across your entire library
- **Playlist Comparison** — compare two playlists side by side, see shared songs and unique songs in each

---

## Tech Stack

- **Python**
- **Streamlit** — web UI
- **Spotipy** — Spotify API wrapper
- **Pandas** — data processing
- **Spotify Web API** — playlist and track data

---

## Screenshots

> Add screenshots here

---

## Run Locally

1. Clone the repo
```bash
   git clone https://github.com/harshithaa-p/Sortify.git
   cd Sortify
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the root folder
```
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8501
```

4. Run the app
```bash
   streamlit run app.py
```

---

## Spotify API Note

This app is currently in **Development Mode** on Spotify. If you'd like to try it, contact me to get whitelisted. Extended Quota Mode approval is pending which will open access to everyone.

---

## Author

Made by [Harshithaa](https://github.com/harshithaa-p)