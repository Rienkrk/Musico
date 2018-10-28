from flask import Flask, render_template
import json
from rdflib import Graph, RDF, Namespace, Literal, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
import pprint as pp
from random import shuffle
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/artist/<artist>")
def artist(artist):

	desc = "Geen beschrijving beschikbaar."
	rating = '4'
	national= 'Niet bekend'
	died = 'Niet bekend'
	born = 'Niet bekend'
	function = 'Niet bekend'
	imageLink = ""

	sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
	sparql.setQuery(
		"""
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX mo: <http://purl.org/ontology/mo/>
		SELECT ?brainzLink
		WHERE {
			?sub foaf:name "%s" .
			?sub mo:musicbrainz ?brainzLink
		}
		"""
	% (artist)) 
	sparql.setReturnFormat(JSON)
	response = sparql.query().convert()
	for result in response["results"]["bindings"]:
		brainzLink = result['brainzLink']['value']

	sparqlt = SPARQLWrapper("http://dbpedia.org/sparql")
	sparqlt.setQuery(
		"""
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX dct: <http://purl.org/dc/terms/>

		SELECT ?description ?national ?died ?born ?imageLink ?function WHERE {
			?sub foaf:name "%s"@en .
			OPTIONAL { ?sub dbo:birthPlace ?city } .
			OPTIONAL { ?city dbo:country ?country } .
			OPTIONAL { ?country dbo:demonym ?national } .
			OPTIONAL { ?sub dbo:deathDate ?died } .
			OPTIONAL { ?sub dbo:birthDate ?born } .
			OPTIONAL { ?sub dbo:abstract ?description } .
			OPTIONAL { ?sub dbo:thumbnail ?imageLink } . 
			OPTIONAL { ?sub dct:description ?function } .
			FILTER (LANG(?description)='nl')
		} 
		"""
	% (artist)) 
	sparqlt.setReturnFormat(JSON)
	responset = sparqlt.query().convert()
	for result in responset["results"]["bindings"]:
		if 'description' in result:
			desc = result['description']['value']
		if 'national' in result:
			national = result['national']['value']
		if 'died' in result:
			died = result['died']['value']
		if 'born' in result:
			born = result['born']['value']
		if 'imageLink' in result:
			imageLink = result['imageLink']['value']
		if 'function' in result:
			function = result['function']['value']

	uid = brainzLink[30:]

	response = requests.get("http://musicbrainz.org/ws/2/artist/"+uid+"?inc=releases+url-rels+tags+ratings&fmt=json")
	if response.status_code == 200:
		artistData = response.json()

	rating = artistData['rating']['value']

	links = {}
	for x in artistData['relations']:
		link = x['url']['resource']
		if 'spotify' in link:
			links['Spotify'] = link
		if 'itunes' in link:
			links['Itunes'] = link
		if 'last.fm' in link:
			links['Last FM'] = link
		if 'bbc' in link:
			links['BBC'] = link
	tags = []
	for tag in artistData['tags']:
		tags.append(tag['name'])

	artistAlbums = {}
	for releases in artistData['releases']:
		response = requests.get("http://coverartarchive.org/release/" + releases['id'])
		if(response.status_code == 200):
			releaseData = response.json()
			artistAlbums[releases['title']] = releaseData['images'][0]['image']

		if len(artistAlbums) == 3:
			break
	print(tags)
	return render_template("artist.html", artist=artist, links=links, artistAlbums=artistAlbums, desc=desc, tags=tags, rating=rating, national=national, died=died, born=born, imageLink=imageLink, function=function) 

@app.route("/album/<album>")
def album(album):

	lang = "none"
	imageLink = "none"
	date = "none"
	amazonLink = "none"
	maker = "none"
	contains = "none"
	lent = "none"
	musicLink = "none"

	album = album.replace("%2F", "/")

	sparql = SPARQLWrapper("http://localhost:5820/musico/query")
	sparql.setQuery(
		"""
		SELECT ?sub ?lang ?imageLink ?date ?amazonLink ?maker ?contains ?len ?musicLink
		WHERE {
			?sub dc:title "%s" .
			OPTIONAL { ?sub dc:language ?langLink } .
			OPTIONAL { <?langLink> rdfs:label ?lang } .
			OPTIONAL { ?sub mo:image ?imageLink } .
			OPTIONAL { ?sub dc:date ?date } .
			OPTIONAL { ?sub mo:amazon_asin ?amazonLink } .
			OPTIONAL { ?sub foaf:maker ?test } . 
			OPTIONAL { ?test foaf:name ?maker } . 
			OPTIONAL { ?sub mus:contains ?contains } .
			OPTIONAL { ?contains mo:length ?len } .
			OPTIONAL { ?sub mo:musicbrainz ?musicLink }
		}
		"""
	% (album)) 
	
	sparql.setReturnFormat(JSON)
	response = sparql.query().convert()
	for result in response["results"]["bindings"]:

		sub = result['sub']['value']

		if 'lang' in result:
			lang = result['lang']['value']
		if 'imageLink' in result:
			imageLink = result['imageLink']['value']
		if 'date' in result:
			date = result['date']['value']
		if 'amazonLink' in result:
			amazonLink = result['amazonLink']['value']
		if 'maker' in result:
			maker = result['maker']['value']
		if 'contains' in result:
			contains = result['contains']['value']
		if 'len' in result:
			lent = result['len']['value']
		if 'musicLink' in result:
			musicLink = result['musicLink']['value']


	uid = sub[46:]
	print(uid)

	response = requests.get("http://musicbrainz.org/ws/2/release/"+uid+"?inc=artist-credits+discids+tags+recordings&fmt=json")
	print(response.status_code)
	if response.status_code == 200:
		albumData = response.json()

		tags = []
		for x in albumData['tags']:
			tags.append(x['name'])

		artists = []
		for x in albumData['artist-credit']:
			artists.append(x['artist']['name'])

		amount = albumData['media'][0]['track-count']

		tracks = []
		for x in albumData['media'][0]['tracks']:
			tracks.append(x['title'])

	return render_template("album.html", album=album, language=lang, imageLink=imageLink, date=date, amazonLink=amazonLink, maker=maker, tracks=tracks, artists=artists, tags=tags, amount=amount)

@app.route("/track/<track>")
def track(track):

	length = "Niet bekend"

	sparqlt = SPARQLWrapper("http://localhost:5820/musico/query")
	sparqlt.setQuery(
		"""
		SELECT ?length ?musicbrainzLink
		WHERE {
			?sub dc:title "%s" .
			OPTIONAL { ?sub mo:length ?length } .
  			OPTIONAL { ?sub mo:musicbrainz ?musicbrainzLink } .
		} 
		"""
	% (track)) 

	sparqlt.setReturnFormat(JSON)
	responset = sparqlt.query().convert()
	for result in responset["results"]["bindings"]:
		if 'length' in result:
			length = result['length']['value']
		if 'musicbrainzLink' in result:
			musicbrainzLink = result['musicbrainzLink']['value']

	uid = musicbrainzLink[29:]
	print(uid)
	response = requests.get("http://musicbrainz.org/ws/2/recording/"+uid+"?inc=artist-credits+releases+tags&fmt=json")
	if response.status_code == 200:
		trackData = response.json()

		artist = trackData['artist-credit'][0]['name']
		date = trackData['releases'][0]['date']

		trackAlbums = {}
		for releases in trackData['releases']:
			response = requests.get("http://coverartarchive.org/release/" + releases['id'])
			if(response.status_code == 200):
				releaseData = response.json()
				trackAlbums[releases['title']] = releaseData['images'][0]['image']

		tags = []
		for tag in trackData['tags']:
			tags.append(tag['name'])

	return render_template("track.html", track=track, trackAlbums=trackAlbums, tags=tags, artist=artist, date=date, length=length)

@app.route("/search/<query>", methods=['GET', 'POST'])
def search(query):
	results = []
	options = []

	sparqlx = SPARQLWrapper("http://localhost:5820/musico/query")
	sparqlx.setQuery("""
		SELECT ?name
		WHERE {
			?sub rdf:type cmno:Composer .
			?sub foaf:name ?name
		}
	""")
	sparqlx.setReturnFormat(JSON)
	responseX = sparqlx.query().convert()
	for result in responseX["results"]["bindings"]:
		options.append({"category": "artist", "name": result['name']['value']})

	sparqlz = SPARQLWrapper("http://localhost:5820/musico/query")
	sparqlz.setQuery("""
		SELECT ?name
		WHERE {
			?sub rdf:type mo:MusicArtist .
			?sub foaf:name ?name
		}
	""")
	sparqlz.setReturnFormat(JSON)
	responseZ = sparqlz.query().convert()
	for result in responseZ["results"]["bindings"]:
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

	sparqls = SPARQLWrapper("http://localhost:5820/musico/query")
	sparqls.setQuery("""
		SELECT ?name
		WHERE {
			?sub rdf:type mus:Track .
			?sub dc:title ?name
		}
	""")
	sparqls.setReturnFormat(JSON)
	responses = sparqls.query().convert()
	for result in responses["results"]["bindings"]:
		options.append({"category": "track", "name": result['name']['value']})

	for option in options:
		if query in option['name'].lower():
			result = {'category': option['category'], 'name': option['name']}
			results.append(result)

	shuffle(results)
	return json.dumps(results[:50])

# Run app
if __name__ == "__main__":
	app.run()
