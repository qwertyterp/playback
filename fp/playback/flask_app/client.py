import base64
import datetime
import os

import requests
from requests import post, get
import json

# credit where credit is due:
# i referenced both of the below resources
# https://www.youtube.com/watch?v=WAmEZBEeNmg
# https://github.com/joseterrera/Spotify-API-with-flask/blob/ff4067b5acfc4bfe1f2c6e31e2d1dd32a67433fa/spotify_requests/spotify.py

CLIENT_ID = "9ae0c155811a4e77bd42962005ff53fd"
CLIENT_SECRET = "cd53d4d5f41c497e979cbdfd8c459371"
class SpotifyAPI(object):

    CLIENT_ID = "9ae0c155811a4e77bd42962005ff53fd"
    CLIENT_SECRET = "cd53d4d5f41c497e979cbdfd8c459371"
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    
    def __init__(self):
        # self.sess = requests.session
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET

    # similar to get_token from yt vid
    def perform_auth(self):
        auth_string = self.CLIENT_ID + ":" + self.CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        now  = datetime.datetime.now()
        access_token = json_result["access_token"]
        expires_in = json_result["expires_in"] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if token == None:
            self.perform_auth()
            return self.get_access_token()
        elif expires < now:
            self.perform_auth()
            return self.get_access_token()

        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        return {"Authorization": "Bearer " + access_token}

    # gives the top 30 results
    def seach_for_artist_info(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_resource_header()
        # general format: f"?q={<your search query>}&type=<comma delimited list of things you are searching for e.g. artist, album, track>&limit=<uppper bound of results you want>"
        query = f"?q={artist_name}&type=artist&limit=30"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            return None
        return json_result
    
    def get_artist_info_by_artist_id(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = self.get_resource_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    def get_albums_info_by_artist_id(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        headers = self.get_resource_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result
    
    def get_track_info_by_album_id(self, album_id):
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        headers = self.get_resource_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result
    
    def get_album_info_by_album_id(self, album_id):
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = self.get_resource_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    



# ## Testing API ###
# client = SpotifyAPI()
# print(client.get_access_token())
# result = client.seach_for_artist_info("Pink Floyd")
# # get artists by a query
# for artist in result:
#     print(artist['name'])
#     print(artist['genres'])
#     print("artist_id", artist["id"])

# # get all albums by artist ID
# artist_id = result[0]['id']
# albums_info = client.get_albums_info_by_artist_id(artist_id)
# for album in albums_info:
#     print(album["name"])

# # get all tracks by album
# artist_id = result[0]['id']
# albums_info = client.get_albums_info_by_artist_id(artist_id)
# album_id = albums_info[0]['id']
# album_info = client.get_track_info_by_album_id(album_id)
# for track in album_info:
#     print(track['name'])

# artist_name = client.get_artist_info_by_artist_id(artist_id)["name"]
# print(artist_name)
