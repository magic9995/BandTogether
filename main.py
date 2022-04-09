import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class User:

    attributes = None
    topSongs = None
    userName = None

    def __init__(self):

        ## Authenticate Spotify Account
        scope = "user-top-read user-read-private"

        sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope=scope, 
<<<<<<< HEAD
                    client_id='315f3c2cf8284851aa92016e7b0a8650',
                    client_secret='dfd0dcf6d9b844a09a5cf3774f1720c6',
=======
                    client_id='2389dfc7a35846509d76f95c5f37c15a',
                    client_secret='972e17031c6744c0b668b4157e656bf6',
>>>>>>> 678c6d9501a8687a87c6f53a0a0b55018bd9239a
                    redirect_uri='http://localhost:7777/callback',
                    open_browser=True,
                    show_dialog=True))
        
        ## First get the top tracks using spotify API
        ## This gives us a dictionary, which I convert to a pandas DataFrame called "tracks"
        ## Then I get all the attributes for the top tracks and put them in a pandas DataFrame 
        ## which I call "analysis". Then I get the mean for each category and standardize them

        topTracks = sp.current_user_top_tracks(limit = 20, time_range="long_term")
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

        ## Get User's username
        profile = sp.current_user()
        self.userName = profile['display_name']

    def getSongData(self):

        return self.attributes

    def getTopSongs(self):

        return self.topSongs

    def getName(self):

        return self.userName

class App:

    def __init__(self):

        pass

    def getUserData(self):

        pass

    def Login(self):

        pass

    def compare(self, user1, user2):

        ## Algorithm for getting difference is following:
        ## Sum for all attributes i: 
        ## (user1.attribute_i - user2.attribute_i) ^ 2

        diff = 0

        for attribute in user1.attributes.keys():
            sum += user1.attributes[attribute] - user2.attributes[attribute]
            diff += sum ** 2

        return diff

    def enterInDB(self, User):

        pass
