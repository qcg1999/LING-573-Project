from argparse import ArgumentParser
from utils.logger import log_info
from features.topic_clusters import find_topic_clusters
from features.content_realization import *
from features.features_from_doc import *
from algorithms.textrank import textrank
from algorithms.entity_grid import * 
from algorithms.compressor import * 
from algorithms.person_name_simplifier import *
import os, operator
import pickle

parser = ArgumentParser()
parser.add_argument("--schema", type=str, required=True)
parser.add_argument("--aquaint", type=str, default="/corpora/LDC/LDC02T31")
parser.add_argument("--aquaint2", type=str, default="/corpora/LDC/LDC08T25")
parser.add_argument("--gigaword", type=str, default="/corpora/LDC/LDC11T07")
parser.add_argument("--output_dir", type=str, default='../outputs/D4')
parser.add_argument("--mode", type=str, choices=['train','dev','eval'], default='train')
parser.add_argument("--store", type=str, default=None)
parser.add_argument("--load", type=str, default=None)

# CoreNLP configs
parser.add_argument("--stanford_home", type=str, default="/NLP_TOOLS/parsers/stanford_parser/latest")
parser.add_argument("--model_path", type=str, default='/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz')
parser.add_argument("--parser_jar", type=str, default='/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar')

args, unks = parser.parse_known_args()

def main():	
	log_info("Finding document clusters for %s mode..." % args.mode)
	topic_clusters = find_topic_clusters(args.schema, (args.aquaint, args.aquaint2, args.gigaword), args.mode)
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

	#put clusters in specific order for consistent behavior across environments
	topic_clusters = sorted(topic_clusters.items(), key=operator.itemgetter(0))

	for index,(topic, docs) in enumerate(topic_clusters):
		log_info("Processing cluster %s..." % topic)

		if args.load:
			sentences, feature_vectors = data[index]
		else:
			if args.aquaint in docs[0][0]:
				sentences, feature_vectors = get_features(docs, 1)
			elif args.aquaint2 in docs[0][0]:
				sentences, feature_vectors = get_features(docs, 2)
			else:
				sentences, feature_vectors = get_features(docs, 3)
			data[index] = (sentences, feature_vectors)

		log_info("textrank starting...")
		sents = [r[1] for r in textrank(feature_vectors,sentences)]

		#compress
		log_info("compress sentences ...")
		sents = compress_sents(sents)

		#truncate
		sents = truncate(sents)
	
		#order
		log_info("get_ordered_sentences starting..." )
		sents = get_ordered_sentences(sents)
		print("ranked_sentences\n", sents)

		#simplify person names
		log_info("compress sentences ...")
		sents = simplify_names(sents)
		
		
		log_info("realize starting...")
		summary = realize2(sents)
		print("summary: \n", summary)

		summary_file = "{0}/{1}-A.M.100.{2}.0".format(args.output_dir, topic[:-1], topic[-1])

		log_info("creating summary file {0}".format(summary_file) )

		f = open(summary_file, "w+")
		f.write(summary)
		f.close()

	if args.store:
		write_file = open(args.store, "wb+")
		pickle.dump(data, write_file)
		write_file.close()

if __name__ == "__main__":
	main()
