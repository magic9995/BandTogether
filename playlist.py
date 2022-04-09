import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2389dfc7a35846509d76f95c5f37c15a",
                                               client_secret="972e17031c6744c0b668b4157e656bf6",
                                               redirect_uri="http://localhost:7777/callback",
                                               scope="playlist-read-private "))

# results = sp.current_user_playlists()
# print(results)
# # print(results['items'])
# # for idx, item in enumerate(results['items']):
# #     track = item['track']
# #     print(idx, track['artists'][0]['name'], " – ", track['name'])

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':
    playlists = sp.current_user_playlists()
    print(playlists)
    for playlist in playlists['items']:
        print()
        print(playlist['name'])
        print ('  total tracks', playlist['tracks']['total'])
        results = sp.playlist(playlist['id'],
        fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks)