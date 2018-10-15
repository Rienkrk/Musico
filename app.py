from flask import Flask, render_template

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

@app.route("/")
def index():
    return render_template("index.html")

# Run app
if __name__ == "__main__":
    app.run()