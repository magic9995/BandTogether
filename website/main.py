#from wsgiref.util import request_uri
from flask import Flask, request, render_template
from app import User, App

app = Flask(__name__)
app.config['HOSTNAME'] = "Rohan"
@app.route('/')
def index():

   return render_template("index.html")

@app.route('/load')
def load():

   return render_template("load.html")

@app.route('/loading', methods=['POST'])
def dashboard():

   if request.method == 'POST':
      username = request.form["email"]
      password = request.form["password"]
      
   user = User()
   appl = App()
   info = appl.getTopAlbumsArtists(user)
   albums = info[0]
   artists = info[1]
   images = []
   for link in albums.keys():
      images.append(albums[link])
   
   topArtists = []
   for artist in artists.keys():
      topArtists.append(artist)

   return render_template("loading.html", username=username, password=password, images=images,
                           artists = topArtists, lenArtists = len(artists))

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', threaded=True)
