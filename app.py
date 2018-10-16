from flask import Flask, render_template

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ArtistPage")
def ArtistPage():
    return render_template("ArtistPage.html")

@app.route("/GenrePage")
def GenrePage():
    return render_template("GenrePage.html")

@app.route("/SongPage")
def SongPage():
    return render_template("SongPage.html")

# Run app
if __name__ == "__main__":
    app.run()