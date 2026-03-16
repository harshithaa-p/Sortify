import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from dotenv import load_dotenv

load_dotenv()

SCOPE = "playlist-read-private playlist-read-collaborative"

def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=None,
        show_dialog=True
    )

def get_spotify_client():
    auth_manager = get_auth_manager()
    code = st.query_params.get("code")

    if code and 'token_info' not in st.session_state:
        try:
            token_info = auth_manager.get_access_token(code, as_dict=True)
            st.session_state['token_info'] = token_info
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")
            return None

    if 'token_info' not in st.session_state:
        return None

    token_info = st.session_state['token_info']

    if auth_manager.is_token_expired(token_info):
        try:
            token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
            st.session_state['token_info'] = token_info
        except:
            st.session_state.clear()
            st.rerun()

    return spotipy.Spotify(auth=token_info['access_token'])

def login_button():
    auth_manager = get_auth_manager()
    auth_url = auth_manager.get_authorize_url()
    st.link_button("Login with Spotify 🎵", auth_url)