#!/usr/bin/env python

from argparse import ArgumentParser
from logger import log_info
from topic_clusters import find_topic_clusters
#from get_features import *
#from summarize import *

parser = ArgumentParser()
parser.add_argument("--schema", type=str, required=True)
parser.add_argument("--aquaint", type=str, default="/corpora/LDC/LDC02T31")
parser.add_argument("--aquaint2", type=str, default="/corpora/LDC/LDC08T25")
parser.add_argument("--mode", type=str, choices=['train','dev','eval'],default='train')
args, unks = parser.parse_known_args()

def main():	
	log_info("Finding document clusters for %s mode..." % args.mode)
	'''topic_clusters is a dictionary of the form:
		key: topic id
		value: tuple(absolute file path, reference id)
	
		The reference id should be used to extract the correct XML block in the source file
	'''
	topic_clusters = find_topic_clusters(args.schema, (args.aquaint, args.aquaint2), args.mode)
	log_info("Found %d document clusters." % len(topic_clusters))

	# get list of feature vectors (for now, just plain text).
	# feature_vectors should be an n by f 2d array where f is the number of features per topic.
	# For now, f will be the number of documents and each feature will be the full text of 1 document.
	#feature_vectors = get_features.get_features(documents)

	# should create n files with names taken from list ids
	#summarize.summarize(ids, feature_vectors)

if __name__ == "__main__":
	main()
