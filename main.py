from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# SPOTIFY AUTHENTICATION USING SPOTIPY
CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRETS']

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# BEAUTIFULSOUP - WEB SCRAPING TO GET LIST OF TOP SONGS FOR INPUTTED DATE

date = input('Which year would you like to travel to? Type the data in this format, YYYY-MM-DD:')

URL = 'https://www.billboard.com/charts/hot-100/'

response = requests.get(URL+date)
webpage = response.text

soup = BeautifulSoup(webpage, 'html.parser')
songs = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')

song_names = [song.getText() for song in songs]

# GETTING SONG URIS

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# CREATING PLAYLIST AND ADDING SONGS

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
