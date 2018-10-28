import requests
import pprint as  pp

response = requests.get("http://musicbrainz.org/ws/2/recording/589fa78c-63e8-43be-af3d-c423dc79a009?inc=artist-credits+releases+tags&fmt=json")
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
	print(trackAlbums)
	print(tags)
	print(artist)
	print(date)
