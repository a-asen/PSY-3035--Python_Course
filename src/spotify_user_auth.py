# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:49:54 2023

@author: steff


'''
To-do :
    Remixed songs do not have a tag for "remixed", they are all 
'''


"""

##### User authorization to read private and history
# %% packages
import os
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# %% set directory
if os.path.exists("D:/coding/GitHub/a-asen/spotify_project"): # School 
    path = "D:/coding/GitHub/a-asen/spotify_project"
if os.path.exists("D:/_coding/GitHub/a-asen/spotify_project"): # Home
    path = "D:/_coding/GitHub/a-asen/spotify_project"

os.chdir(path)
print(os.getcwd())

#%%  Read Keys
# Get access token # Read JSON
with open("access/access_token.json", "r") as f:
    access_token = json.load(f)

sp_client    = access_token["Client_ID"]            # Client ID
sp_secret    = access_token["Client_Secret"]        # Client Secret
sp_redirect  = "http://localhost:8888/callback"     # Local to grantk access? 
# sp_scopes  = "user-read-recently-played"  # Scopes
sp_scopes    = "user-read-playback-state, user-read-currently-playing, user-read-playback-position, user-top-read, user-read-recently-played, playlist-read-private,playlist-read-collaborative"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/ 
# https://spotipy.readthedocs.io/en/2.22.1/#spotipy.oauth2.SpotifyOAuth.__init__

# %%  Spotify General access credentials 
# This gives us access to public info on Spotify 
# See below for private related data
#sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = sp_client,
#                                                             client_secret = sp_secret))

# %%   Spotify Authentication

# https://spotipy.readthedocs.io/en/2.22.1/#spotipy.oauth2.SpotifyOAuth.__init__
sp_user_auth = spotipy.SpotifyOAuth(
    client_id     = sp_client,    # client ID
    client_secret = sp_secret,    # Secret
    redirect_uri  = sp_redirect,  # redirect to....
    scope         = sp_scopes)    # access scope
    # I suppose this (redirect_uri) is where the data is being sent to, where 
    # we access the data?  Therefore it is also a "local" target. 
    # We might, I guess, put up a server target (https://cross_sync.com:8080/callback) 
    # to handle responses to bigger databases to make apps.
        # redirect_uri  = sp_api_url # redirect to spotify API call
        # Does not work with this code, hence the above

sp_user_auth.get_authorization_code() # Should open the browser

# get_access_token = sp_user_auth.get_access_token() # access token 

# get_auth_url = sp_user_auth.get_authorize_url()() # url response from

# get_auth_response = sp_user_auth.get_auth_response() # get auth response (id?)
# get_auth_code = sp_user_auth.get_authorization_code()  # get auth code

# sp_user_auth.get_cached_token() # get stored file?


# %%  Set the "auth_manager" to our credentials according to the given "auth" access

# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

# We set our access point to "sp" by authorizing with "sp_user_auth" 
sp = spotipy.Spotify(auth_manager = sp_user_auth)

# %%  Get Recently Played

# See documentation:
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recently-played
user_recently_played = sp.current_user_recently_played() # get users last played (limit = 50)


# %% Get recently played
dl_recently = []
for item in user_recently_played["items"]:
    d = {}
    d["played_time"]    = item["played_at"]
    d["track_title"]    = item["track"]["name"]
    d["artists"] = []
    for artist in item["track"]["artists"]:
        d["artists"].appen(artist["name"])
    d["popularity"]     = item["track"]["popularity"]
    d["uri"]            = item["track"]["uri"]
    d["duration"]       = item["track"]["duration_ms"]
    dl_recently.append(d)
       
df_recently = pd.DataFrame(dl_recently)
        
# %%  Get "a" playlist tracks 
# does not get out

playlist_tracks = sp.playlist_tracks("2vNB2I9nXt9oqCgq7VQ2tn") # 2022 playlist

dl_playlist = []
for item in playlist_tracks["items"]:
    d = {}
    d["track_title"]       = item["track"]["name"]
    d["artists"]           = []
    for artist in item["track"]["artists"]:
        d["artists"].append(artist["name"])
    d["popularity"]        = item["track"]["popularity"]
    d["uri"]               = item["track"]["uri"]
    d["duration"]          = item["track"]["duration_ms"]
    d["added_by"]          = item["added_by"]["id"]
    d["added_at"]          = item["added_at"]
    
df_playlist = pd.DataFrame(dl_playlist)

# %%  Top artists
top_artists = sp.current_user_top_artists()

dl_artists = []
for item in top_artists["items"]:
    d = {}
    d["name"]     =   item["name"]
    d["popularity"]     =   item["popularity"]
    d["genres"]     =   item["genres"]
    dl_artists.append(d)

df_artists = pd.DataFrame(dl_artist)

# %%   Top tracks
top_tracks = sp.current_user_top_tracks(limit = 50)

dl_tracks = []
for item in top_tracks["items"]:
    d = {}
    d["track_title"]    = item["name"]
    da  = []
    for artist in item["artists"]:
        da.append(artist["name"])
    d["artists"]        = da
    d["popularity"]     = item["popularity"]
    d["uri"]            = item["uri"]
    d["duration"]       = item["duration_ms"]
    d["duration"]       = item["images"]["release_dat"]
    dl_tracks.append(d)

df_tracks = pd.DataFrame(dl_tracks)


# %%  Get song analysis

playlist_features = sp.audio_features(df_playlist["uri"])

playlist_features[0].keys()


analysis = sp.audio_analysis("6swKdthrzbQO6HJWl7irWQ")


analysis.keys()
analysis["meta"]
analysis["track"].keys()
analysis["track"]["synchstring"]

analysis["sections"][0].keys()
analysis["sections"][0]["loudness"]


analysis["segments"][0].keys()
zanalysis["segments"][0]
track_analysis = []

for item in analysis["segments"]:
    d = {}
    d[""]

analysis["segments"][0]["loudness_max_time"]
analysis["segments"][0]["loudness_max"]
analysis["segments"][0]["loudness_end"]
analysis["segments"][0]["loudness_max_time"]
analysis["segments"][0]["pitches"]
analysis["segments"][0]["timbre"]







