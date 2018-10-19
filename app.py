from flask import Flask, render_template
import json
from rdflib import Graph, RDF, Namespace, Literal, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/artist/<artist>")
def artist(artist):
    return render_template("artist.html", artist=artist)

@app.route("/genre/<genre>")
def genre(genre):
    return render_template("genre.html")

@app.route("/song/<song>")
def song(song):
    return render_template("song.html")

@app.route("/search/<query>", methods=['GET', 'POST'])
def search(query):
    results = []
    options = []


    sparql = SPARQLWrapper("http://localhost:5820/hqaecua/query")
    sparql.setQuery("""
        SELECT ?name
        WHERE {
            ?sub rdf:type mus:Composer.
            ?sub foaf:name ?name
        }
    """)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    for result in response["results"]["bindings"]:
        options.append(result['name']['value'].lower())

    print(list(set(options)))

    for option in options:
        if query in option:
            result = {'category': 'artist', 'name': option}
            results.append(result)
    return json.dumps(results)

# Run app
if __name__ == "__main__":
    app.run()