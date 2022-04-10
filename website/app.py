from asyncio.windows_events import NULL
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import CockroachConnection as dbUser
import CocroachConnectenTable2 as dbSpotify

class User:

    attributes = None
    topSongs = None
    userName = None

    def __init__(self):

        ## Authenticate Spotify Account
        scope = "user-top-read user-read-private"

        sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope=scope, 
                    client_id='ce9afb29e4284a729918445e8e9be2e0',
                    client_secret='32f4053e166249dfbf307a029658eb58',
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
        analysis['loudness'] = abs(analysis['loudness'])

        ## Set class variables

        self.attributes = analysis.to_dict()
        self.topSongs = tracks

        ## Get User's username
        profile = sp.current_user()
        self.userName = profile['display_name']

        test = App()
        print(test.getTopAlbumsArtists(self))

    def getSongData(self):

        return self.attributes

    def getTopSongs(self):

        return self.topSongs

    def getName(self):

        return self.userName

class App:

    userConn = None
    spotifyConn = None

    def __init__(self):

        self.userConn = dbUser.getConn()
        self.spotifyConn = dbSpotify.getConn()

    def insertUserSongData(self, user: User, username):

        if dbSpotify.containsUser(self.spotifyConn, username):

            userExistData = dbSpotify.returnSpotifyDataOfUsername(self.spotifyConn, username)
            dbSpotify.modifySpotifyData(self.spotifyConn, [username, user.attributes['liveness'], user.attributes['valence'],
                                    user.attributes['danceability'], user.attributes['loudness'], 
                                    user.attributes['mode'], user.attributes['acousticness'], 
                                    user.attributes['instrumentalness'], user.attributes['tempo'],
                                    user.attributes['energy'], userExistData['latitude'], 
                                    userExistData['longititude']])
            
        else:

            dbSpotify.insertData(self.spotifyConn, username, user.attributes['liveness'], user.attributes['valence'],
                                    user.attributes['danceability'], user.attributes['loudness'], 
                                    user.attributes['mode'], user.attributes['acousticness'], 
                                    user.attributes['instrumentalness'], user.attributes['tempo'],
                                    user.attributes['energy'], 'NULL', 'NULL')
            
    def insertLocation(self, username, latitude, longitude):

        if dbSpotify.containsUser(self.spotifyConn, username):

            userExistData = dbSpotify.returnSpotifyDataOfUsername(self.spotifyConn, username)
            dbSpotify.modifySpotifyData(self.spotifyConn, username, [username, userExistData['liveness'], 
                                    userExistData['valence'],
                                    userExistData['danceability'], userExistData['loudness'], 
                                    userExistData['mode'], userExistData['acousticness'], 
                                    userExistData['instrumentalness'], userExistData['tempo'],
                                    userExistData['energy'], latitude, 
                                    longitude])
            
        else:

            raise Exception("Account does now exist")

    def SignUp(self, username, password):
        if not dbUser.containsUser(self.userConn, username):
            dbUser.insertUser(self.userConn, 'NULL', password,
                              'NULL', username, 'NULL')
        else:
            raise Exception("User already exists")

    def compare(self, user1: User, user2: User):

        ## Algorithm for getting difference is following:
        ## Sum for all attributes i: 
        ## (user1.attribute_i - user2.attribute_i) ^ 2

        diff = 0

        for attribute in user1.attributes.keys():
            sum += user1.attributes[attribute] - user2.attributes[attribute]
            diff += sum ** 2

        return diff

    def enterInDB(self, user):

        pass

    def getTopAlbumsArtists(self, user: User):

        artists = {}
        albums = {}

        userAlbums = user.getTopSongs()
        for track in userAlbums.iterrows():
        
            index = track[0]
            info = track[1]

            if len(albums.keys()) < 6:
                if albums.get(info['album']['name']) == None:
                    albums[info['album']['name']] = info['album']['images'][0]['url']

            if len(artists.keys()) < 6:
                if artists.get(info['album']['artists'][0]['name']) == None:
                    artists[info['album']['artists'][0]['name']] = info['album']['artists'][0]['name']
            
        return (albums, artists)