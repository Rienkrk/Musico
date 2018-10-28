import requests
import pprint as  pp

# for s in testkees['images']:
        # print(s['image'])

# pp.pprint(response)

# https://wiki.musicbrainz.org/Development/JSON_Web_Service 
# https://musicbrainz.org/recording/a389b369-0d22-48de-8edd-8e9952ea3468

# testkees = requests.get("http://coverartarchive.org/release/24f1766e-9635-4d58-a4d4-9413f9f98a4c")

    # resp = requests.get("http://musicbrainz.org/ws/2/release/" + x['id'] + "?inc=&fmt=json")
    # if(resp.status_code == 200):
    #     resp = resp.json()
    #     # pp.pprint(resp)
    # print(x['id'])
    # pp.pprint(x)

    # Request: http://musicbrainz.org/ws/2/artist/05cbaf37-6dc2-4f71-a0ce-d633447d90c3?inc=tags+ratings&fmt=jso

# ?inc=artist-credits+labels+discids+recordings&fmt=json
# releases+


response = requests.get("http://musicbrainz.org/ws/2/artist/24f1766e-9635-4d58-a4d4-9413f9f98a4c?inc=releases+url-rels+ratings+tags&fmt=json")
if response.status_code == 200:
    artistData = response.json()

for tag in artistData['tags']:
    if tag['count'] > 3:
        print(tag['name'])

print(artistData['rating']['value'])

for x in artistData['relations']:
    link = x['url']['resource']
    if 'spotify' in link:
        spotify = link
    if 'itunes' in link:
        itunes = link
    if 'last.fm' in link:
        lastfm = link
    if 'bbc' in link:
        bbc = link

print(spotify)
print(itunes)
print(lastfm)
print(bbc)

artistAlbums = {}
for releases in artistData['releases']:
    response = requests.get("http://coverartarchive.org/release/" + releases['id'])
    if(response.status_code == 200):
        releaseData = response.json()
        artistAlbums[releases['title']] = releaseData['images'][0]['image']

    if len(artistAlbums) == 3:
        break

pp.pprint(artistAlbums)