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

@app.route("/album/<album>")
def album(album):

    album = album.replace("%2F", "/")

    sparql = SPARQLWrapper("http://localhost:5820/musico/query")
    sparql.setQuery(
        """
        SELECT ?lang ?imageLink ?date ?amazonLink
        WHERE {
            ?sub dc:title "%s" .
            ?sub dc:language ?lang .
            ?sub mo:image ?imageLink .
            ?sub dc:date ?date .
            ?sub mo:amazon_asin ?amazonLink
        }
        """
    % (album)) 
    
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    for result in response["results"]["bindings"]:
        print(result)
        lang = result['lang']['value']
        imageLink = result['imageLink']['value']
        date = result['date']['value']
        amazonLink = result['amazonLink']['value']

    return render_template("album.html", album=album, language=lang, imageLink=imageLink, date=date, amazonLink=amazonLink)

@app.route("/song/<song>")
def song(song):
    return render_template("song.html")

@app.route("/search/<query>", methods=['GET', 'POST'])
def search(query):
    results = []
    options = []

    sparqlx = SPARQLWrapper("http://localhost:5820/musico/query")
    sparqlx.setQuery("""
        SELECT ?name
        WHERE {
            ?sub rdf:type mus:Composer .
            ?sub foaf:name ?name
        }
    """)
    sparqlx.setReturnFormat(JSON)
    responseX = sparqlx.query().convert()
    for result in responseX["results"]["bindings"]:
        options.append({"category": "artist", "name": result['name']['value']})

    sparql = SPARQLWrapper("http://localhost:5820/musico/query")
    sparql.setQuery("""
        SELECT ?name
        WHERE {
            ?sub rdf:type mus:Album .
            ?sub dc:title ?name
        }
    """)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    for result in response["results"]["bindings"]:
        options.append({"category": "album", "name": result['name']['value']})

    for option in options:
        if query in option['name'].lower():
            result = {'category': option['category'], 'name': option['name']}
            results.append(result)
    return json.dumps(results)

# Run app
if __name__ == "__main__":
    app.run()
