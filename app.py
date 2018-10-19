from flask import Flask, render_template
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/artist/<artist>")
def artist(artist):
    return render_template("artist.html")

@app.route("/genre/<genre>")
def genre(genre):
    return render_template("genre.html")

@app.route("/song/<song>")
def song(song):
    return render_template("song.html")

@app.route("/search/<query>", methods=['GET', 'POST'])
def search(query):
    results = []
    # options = ['rock', 'house', 'pop', 'houdie', 'ixconxpop']
    options = [
            "2s","3s","4s","5s","6s","7s","8s","9s","10s","Js","Qs","Ks","As"
            "2h","3h","4h","5h","6h","7h","8h","9h","10h","Jh","Qh","Kh","Ah"
            "2d","3d","4d","5d","6d","7d","8d","9d","10d","Jd","Qd","Kd","Ad"
            "2c","3c","4c","5c","6c","7c","8c","9c","10c","Jc","Qc","Kc","Ac"
           ]

    for option in options:
        if query in option:
            result = {'category': 'genre', 'name': option}
            results.append(result)
    return json.dumps(results)

# Run app
if __name__ == "__main__":
    app.run()