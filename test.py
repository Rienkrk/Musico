# import rdflib
# from rdflib import Literal, URIRef
# g1=rdflib.Graph()
# g1.parse('ontology.ttl',format='turtle')
# qres = g1.query(
#    """
#     PREFIX dc: <http://purl.org/dc/elements/1.1/>
#    SELECT ?name
#        WHERE {
#            ?sub rdf:type mus:Composer.
#            ?sub foaf:name ?name
#        }
#       """)

# for row in qres:
#     print('%s', row)

from rdflib import Graph, RDF, Namespace, Literal, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:5820/hqaecua/query")
sparql.setQuery("""
    SELECT ?name
       WHERE {
           ?sub rdf:type mus:Composer.
           ?sub foaf:name ?name
       }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print(result['name']['value'])