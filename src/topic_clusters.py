# jrdodson
'''topic cluster utilities
'''

from BeautifulSoup import BeautifulSoup as soup
from logger import log_warn
import os, fnmatch

def resolve_training_paths(clusters,corpora):
	aquaint, aquaint2 = corpora
	resolved = dict()
	for topic, cluster in clusters.iteritems():		
		absolute_paths = []
		for doc,identifier in cluster:
			path = [os.path.join(path,f) 
				for path,names,files in os.walk(aquaint2) 
				for f in fnmatch.filter(files, "%s.xml" % doc.lower())]
			if len(path) > 1:
				log_warn("Found multiple source files for %s ..." % doc)
			absolute_paths += [(path[0],identifier)]
		if len(absolute_paths) != len(cluster):
			log_warn("Mismatch between raw/resolved clusters...")
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
		tree = soup(schema_handler)
		for topic in tree.findAll("topic"):
			topic_key = topic['id']
			docs = retrieve_docs(topic)
			clusters[topic_key] = docs
	if mode == "train":
		return resolve_training_paths(clusters,corpora)
	else:
		raise ValueError("Unsupported mode")
