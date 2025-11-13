import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlists = sp.user_playlists('spotify')

    playlist_link = "https://open.spotify.com/playlist/1eQ2qqs4cTHcHGsCYZMMEy"
    playlist_URI = playlist_link.split("/")[4]

    spotify_data = sp.playlist_tracks(playlist_URI)

    client = boto3.client('s3')

    filename = "spotify_raw_" + str(datetime.now()) + ".json"

    client.put_object(
        Bucket="spotify-etl-project-tejasb",
        Key="raw_data/to_process/"+ filename,
        Body=json.dumps(spotify_data)
    )