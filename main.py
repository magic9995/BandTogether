import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class User:

    attributes = None
    topSongs = None

    def __init__(self):

        ## Authenticate Spotify Account
        scope = "user-top-read"

        sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope=scope, 
                    client_id='2389dfc7a35846509d76f95c5f37c15a',
                    client_secret='972e17031c6744c0b668b4157e656bf6',
                    redirect_uri='http://localhost:7777/callback',
                    open_browser=True,
                    show_dialog=True))
        
        ## First get the top tracks using spotify API
        ## This gives us a dictionary, which I convert to a pandas DataFrame called "tracks"
        ## Then I get all the attributes for the top tracks and put them in a pandas DataFrame 
        ## which I call "analysis". Then I get the mean for each category and standardize them

        topTracks = sp.current_user_top_tracks(limit = 20, time_range="medium_term")
        tracks = pd.DataFrame.from_dict(topTracks['items'])[['id', 'name', 'album']]
        analysis = pd.DataFrame(sp.audio_features(tracks['id'].to_list()))
        analysis = analysis.mean(axis = 0)[['liveness', 'valence', 'danceability', 'loudness', 'mode',
                                        'acousticness', 'instrumentalness', 'liveness', 'valence', 
                                        'tempo', 'energy']]
        analysis['loudness'] /= 60
        analysis['tempo'] /= 200

        ## Set class variables

        self.attributes = analysis.to_dict()
        self.topSongs = tracks
        print("attributes")
        print(self.attributes)
        print(tracks)

    def getSongData(self):

        return self.attributes

    ## Insert functions here

class App:

    def __init__(self):

        pass

    def getUserData(self):

        pass

    def Login(self):

        pass

    def compare(self, sser1, sser2):

        pass

    def enterInDB(self, User):

        pass
