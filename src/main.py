from argparse import ArgumentParser
from utils.logger import log_info
from features.topic_clusters import find_topic_clusters
from features.content_realization import *
from features.features_from_doc import *
from algorithms.textrank import textrank
from algorithms.entity_grid import entity_grid_order
import algorithms.SummaryGenerator
import os
import pickle

parser = ArgumentParser()
parser.add_argument("--schema", type=str, required=True)
parser.add_argument("--aquaint", type=str, default="/corpora/LDC/LDC02T31")
parser.add_argument("--aquaint2", type=str, default="/corpora/LDC/LDC08T25")
parser.add_argument("--output_dir", type=str, default='outputs/D3')
parser.add_argument("--mode", type=str, choices=['train','dev','eval'],default='train')
parser.add_argument("--store", type=str, default=None)
parser.add_argument("--load", type=str, default=None)

# CoreNLP configs
parser.add_argument("--stanford_home", type=str, default="/NLP_TOOLS/parsers/stanford_parser/latest")
parser.add_argument("--model_path", type=str, default='/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz')
parser.add_argument("--parser_jar", type=str, default='/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar')

args, unks = parser.parse_known_args()

def main():	
	log_info("Finding document clusters for %s mode..." % args.mode)
	topic_clusters = find_topic_clusters(args.schema, (args.aquaint, args.aquaint2), args.mode)
	log_info("Found %d document clusters." % len(topic_clusters))

	log_info("Summarizing...")

	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)

	if args.load:
		read_file = open(args.load, "rb")
		data = pickle.load(read_file)
		read_file.close()
	else:
		data = {}

	for index,(topic, docs) in enumerate(topic_clusters.items()):
		log_info("Processing cluster %s..." % topic)

		if args.load:
			sentences, feature_vectors = data[index]
		else:
			sentences, feature_vectors = get_features(docs)
			data[index] = (sentences, feature_vectors)

		ranked_sentences = textrank(feature_vectors,sentences)
		summary_sentences = truncate(ranked_sentences)

#		entity_grid_order(ranked_sentences,args)

		#information ordering step goes here
		
		summary = realize(summary_sentences)
		id1 = topic[:-1]
		id2 = topic[-1]
		f = open("{0}/{1}-A.M.100.{2}.0".format(args.output_dir, id1, id2), "w+")
		f.write(summary)

	if args.store:
		write_file = open(args.store, "wb+")
		pickle.dump(data, write_file)
		write_file.close()

if __name__ == "__main__":
	main()
