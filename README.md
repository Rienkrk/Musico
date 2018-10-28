# Musico
A webapp where people can retrieve information about (classical) music.

How to start the application:
1. Download the repo, make sure static, template, app.py, musico ontology v4.ttl are present
2. Start Stardog
3. Make a database with the exact name 'musico' and make sure the following namespaces are present:

(Standard)
rdf=http://www.w3.org/1999/02/22-rdf-syntax-ns# 

rdfs=http://www.w3.org/2000/01/rdf-schema# 

xsd=http://www.w3.org/2001/XMLSchema# 

owl=http://www.w3.org/2002/07/owl# 

stardog=tag:stardog:api: 

(To be added)
mo=http://purl.org/ontology/mo/ 

dc=http://purl.org/dc/elements/1.1/ 

mus=http://www.musico.org/musico/ 

foaf=http://xmlns.com/foaf/0.1/ 

cmno=http://purl.org/ontology/classicalmusicnav# 

4. Add the file 'musico ontology v4.ttl' to this database
5. Start your IDE and select the folder with the downloaded repo. Keep stardog running
6. Start the flask app with 'python3 app.py' or 'python app.py' in the terminal of your IDE
7. It should give you a webadres to open the application on: http://127.0.0.1:5000/
8. Explore the website
