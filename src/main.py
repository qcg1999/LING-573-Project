#!/usr/bin/env python

from argparse import ArgumentParser
from logger import log_info
from topic_clusters import find_topic_clusters
from features_from_doc import *
import SummaryGenerator

parser = ArgumentParser()
parser.add_argument("--schema", type=str, required=True)
parser.add_argument("--aquaint", type=str, default="/corpora/LDC/LDC02T31")
parser.add_argument("--aquaint2", type=str, default="/corpora/LDC/LDC08T25")
parser.add_argument("--mode", type=str, choices=['train','dev','eval'],default='train')
args, unks = parser.parse_known_args()

loremipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

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
	for topic, docs in topic_clusters.iteritems():
		sentences, feature_vectors = get_features(docs)
	
		sg = SummaryGenerator.SummaryGenerator();  #instantiate object
		#words = nltk.corpus.brown.words(categories='news')
		summary = sg.ToSummary(sentences, feature_vectors)   #generate summary
#		log_info("EXAMPLE SUMMARY: %s " % summary)

		id1 = topic[:-1]
                id2 = topic[-1]
                f = open("../outputs/D2/{0}-A.M.100.{1}.0".format(id1, id2), "w+")
                f.write(summary)

if __name__ == "__main__":
	main()
