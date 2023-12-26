from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input('Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ')
year = date[0:4]
spotify_client_id = os.environ.get('spotify_client_id')
spotify_client_secret = os.environ.get('spotify_client_secret')
redirect_uri = os.environ.get('spotify_redirect_uri')
spotify_username = os.environ.get('spotify_username')
spotify_scope = 'playlist-modify-private'
playlist_name = f'{date} Billboard 100'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=spotify_scope,
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=spotify_username))
user_id = sp.current_user()["id"]
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
title_tags = soup.select("li ul li h3")
titles = [tag.getText().strip() for tag in title_tags]
track_uris = []
for title in titles:
    results = sp.search(f"track: {title} year: {year}")
    try:
        track_uris.append(results["tracks"]["items"][0]["uri"])
    except KeyError:
        print(f'{title} not found')
    except IndexError:
        print(f'{title} not found')

playlist = sp.user_playlist_create(user_id, playlist_name, False)
sp.playlist_add_items(playlist['id'], track_uris)











