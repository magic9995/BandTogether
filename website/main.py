from wsgiref.util import request_uri
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['HOSTNAME'] = "Rohan"
@app.route('/')
def index():

   return render_template("index.html")

@app.route('/loading', methods=['POST'])
def dashboard():

    if request.method == 'POST':
       username = request.form["email"]
       password = request.form["password"]

    return render_template("loading.html", username=username, password=password)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
