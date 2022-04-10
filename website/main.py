#from wsgiref.util import request_uri
from flask import Flask, request, render_template, session, redirect, url_for
from app import User, App
import sys
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Band_Together_Right_Now"
app.config['HOSTNAME'] = "Rohan"

@app.route('/')
def index():

   if session.get("log_in_fail") == True:
      fail = True
   else:
      fail = False

   return render_template("index.html", fail=fail)

@app.route('/login', methods=['POST'])
def login():

   if request.method == 'POST':
      username = request.form["email"]
      password = request.form["password"]
   
   app = App()
   if app.login(username, password):

      session['username'] = username
      session['password'] = password
      session['log_in_fail'] = False
      return redirect(url_for("dashboard"))

   else:

      session['log_in_fail'] = True
      return redirect(url_for("index"))

@app.route('/signup')
def signup():

   if session.get("sign_up_fail") == True:
      fail = True
   else:
      fail = False

   return render_template("signup.html", fail=fail)

@app.route('/register', methods=["POST"])
def register():

   app = App()
   if request.method == 'POST':
      username = request.form["email"]
      password = request.form["password"]
      confirm = request.form["confirm"]
   if password != confirm:
      
      session["sign_up_fail"] = True
      return redirect(url_for("signup"))
   
   app.SignUp(username, password)
   #session["sign_up_fail"] = True
   #return redirect(url_for("signup"))

   session["sign_up_fail"] = False
   session["username"] = username
   session["password"] = password

   return redirect(url_for("dashboard"))

@app.route('/loading')
def dashboard():

   if session.get("username") == None:
      
      return redirect(url_for('index'))

   username = session['username']
   password = session['password']

   ## Get top albums and artists
   try:
      os.remove(".cache")
   except Exception:
      pass
   user = User()
   app = App()

   name = user.getName()
   app.changeName(username, name)
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
   matches = app.getClosest(session['username'])
   matchesFormat = app.getContactInfo(matches)
   print("\n\n\n")
   print(matchesFormat)
   return render_template("match.html", latitude=latitude, longitude=longitude,
                           matches=matchesFormat, lenMatches = len(matches))

@app.route('/logout')
def logout():

   session.pop('username', None)
   return redirect(url_for("index"))


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', threaded=True)
