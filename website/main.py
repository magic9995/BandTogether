#from wsgiref.util import request_uri
from flask import Flask, request, render_template, session, redirect, url_for
from App import User, App
import sys
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Band_Together_Right_Now"
app.config['HOSTNAME'] = "Rohan"
##app.permanent_session_lifetime = timedelta(days=5)

@app.route('/')
def index():

   return render_template("index.html")

@app.route('/loading', methods=['POST'])
def dashboard():

   if request.method == 'POST':
      username = request.form["email"]
      password = request.form["password"]
      
   session['username'] = username
   session['password'] = password

   ## Get top albums and artists
   user = User()
   app = App()

   app.SignUp(username, password)
   app.insertUserSongData(user, username)

   info = app.getTopAlbumsArtists(user)
   albums = info[0]
   artists = info[1]
   images = []
   for link in albums.keys():
      images.append(albums[link])
   
   topArtists = []
   for artist in artists.keys():
      topArtists.append(artist)

   
   session.modified = True

   return render_template("loading.html", username=username, password=password, images=images,
                           artists = topArtists, lenArtists = len(artists))

@app.route('/location', methods=['GET'])
def location():

   if session.get("username") == None:
      
      return redirect(url_for('index'))

   return render_template("location.html")

@app.route('/match', methods=['POST'])
def match():

   if session.get("username") == None:
      
      return redirect(url_for('index'))

   latitude = request.form['latitude']
   longitude = request.form['longitude']

   app = App()
   app.insertLocation(session['username'], latitude, longitude)

   session['latitude'] = latitude
   session['longitude'] = longitude
   
   return render_template("match.html", latitude=latitude, longitude=longitude)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', threaded=True)
