from argparse import ArgumentParser
from utils.logger import log_info
from features.topic_clusters import find_topic_clusters
from features.content_realization import realize
from features.feature_annotator import annotate
from features.features_from_doc import *
from algorithms.textrank import textrank
import algorithms.SummaryGenerator
import os

parser = ArgumentParser()
parser.add_argument("--schema", type=str, required=True)
parser.add_argument("--aquaint", type=str, default="/corpora/LDC/LDC02T31")
parser.add_argument("--aquaint2", type=str, default="/corpora/LDC/LDC08T25")
parser.add_argument("--output_dir", type=str, default='outputs/D3')
parser.add_argument("--mode", type=str, choices=['train','dev','eval'],default='train')
args, unks = parser.parse_known_args()

def main():	
	log_info("Finding document clusters for %s mode..." % args.mode)
	topic_clusters = find_topic_clusters(args.schema, (args.aquaint, args.aquaint2), args.mode)
	log_info("Found %d document clusters." % len(topic_clusters))

	log_info("Summarizing...")

	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)

	for index,(topic, docs) in enumerate(topic_clusters.items()):
		log_info("Processing cluster %s..." % topic)
		sentences, feature_vectors = get_features(docs)
		ranked_sentences = textrank(feature_vectors,sentences)
		
		enriched = annotate(ranked_sentences) # e.g., [(Bob, NN, B-PERSON), .... ]
		
		summary = realize(ranked_sentences)
		id1 = topic[:-1]
		id2 = topic[-1]
		f = open("{0}/{1}-A.M.100.{2}.0".format(args.output_dir, id1, id2), "w+")
		f.write(summary)

if __name__ == "__main__":
	main()
