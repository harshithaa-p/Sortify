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
    
    # Check if we have a code in the URL
    code = st.query_params.get("code")
    
    if code:
        token_info = auth_manager.get_access_token(code, as_dict=True)
        st.session_state['token_info'] = token_info
        st.query_params.clear()
        st.rerun()
    
    if 'token_info' not in st.session_state:
        return None
    
    token_info = st.session_state['token_info']
    
    if auth_manager.is_token_expired(token_info):
        token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
        st.session_state['token_info'] = token_info
    
    return spotipy.Spotify(auth=token_info['access_token'])

def login_button():
    auth_manager = get_auth_manager()
    auth_url = auth_manager.get_authorize_url()
    st.write(f"Debug URL: {auth_url}")
    st.markdown(f'''
        <a href="{auth_url}" target="_top">
            <button style="
                background-color:#1DB954;
                color:white;
                padding:12px 24px;
                border:none;
                border-radius:25px;
                font-size:16px;
                cursor:pointer;
                font-weight:bold;
            ">
                Login with Spotify
            </button>
        </a>
    ''', unsafe_allow_html=True)