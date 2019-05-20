# jrdodson
'''topic cluster utilities
'''
from bs4 import BeautifulSoup as soup
import os, fnmatch

def _resolve_paths(clusters,corpora):
	def traverse(doc,corpus,ext=".xml"):
		path = [os.path.join(path,f)
			for path,names,files in os.walk(corpus)
			for f in fnmatch.filter(files, "%s%s" % (doc,ext))]
		return path
	def preprocess_traverse(identifier, acquaint):
		prefix = identifier[:3]
		if prefix == "XIE":
			prefix = "XIN"
		search = "%s_%s" % (identifier[3:-5],prefix)
		if prefix != "NYT":
			search = "%s_ENG" % search
		return traverse(search,acquaint,ext="")

	aquaint, aquaint2 = corpora
	resolved = dict()
	for topic, cluster in clusters.items():		
		absolute_paths = []
		for doc,identifier in cluster:
			path = traverse(doc.lower(),aquaint2)
			if len(path) == 0:
				path = preprocess_traverse(identifier,aquaint)
			if len(path) != 1:
				continue
			absolute_paths += [(path[0],identifier)]
		resolved[topic] = absolute_paths
	return resolved

def find_topic_clusters(schema,corpora,mode):
	def retrieve_docs(topic_root):
		cluster = []
		for docset in topic_root.findAll("docseta"):
			for doc in docset.findAll("doc"):
				docId = doc['id'][:-7]
				identifier = doc['id']
				cluster += [(docId,identifier)]
		return cluster

	clusters = dict()
	with open(schema,'r') as schema_handler:
		tree = soup(schema_handler,features='lxml')
		for topic in tree.findAll("topic"):
			topic_key = topic['id']
			docs = retrieve_docs(topic)
			clusters[topic_key] = docs
	return _resolve_paths(clusters,corpora)
