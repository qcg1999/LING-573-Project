import pickle
import os
import random
from bs4 import BeautifulSoup
import nltk
from nltk import tree
from nltk.parse import stanford
import numpy as np
from sklearn.linear_model import LogisticRegression

from utils.logger import log_info
from algorithms.compress_utils import *

#Compression corpora downloaded from https://www.jamesclarke.net/research/resources/

WRITTEN_CORPUS_PATH = '/home/emma/compression-corpora/written'
BROADCAST_CORPUS_PATH = '/home/emma/compression-corpora/broadcast/'

USE_BROADCAST = True
USE_WRITTEN = False
MAX_SENTS = 1000

stanford_home   = '/NLP_TOOLS/parsers/stanford_parser/latest/'
model_path              = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
parser_jar              = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

os.environ['CLASSPATH'] = stanford_home

KEEP = 1
PARTIAL = 1
DELETE = 0

def get_corpus_data(path):
    sent_pairs = []
    for filename in os.listdir(path):
        log_info("reading from file {0} ...".format(path+'/'+filename))
        f = open(path+'/'+filename)
        soup = BeautifulSoup(f.read(), "lxml")
        for sentence in soup.findAll("original"):
            compressed = soup.findAll("compressed", id=sentence['id'])[0]
            sent_pairs.append((sentence.text, compressed.text))
    return sent_pairs

#given pair of original and compressed sentences,
#return feature vector and keep/delete label for each node
def extract_training_data(sentence_tuple):
    original, compressed = sentence_tuple
    #get trees
    parser = stanford.StanfordParser (
            model_path = model_path,
            path_to_models_jar = parser_jar
            )
    for p in parser.raw_parse(original):
        original_tree = tree.Tree.fromstring(str(p))
        break
    for p in parser.raw_parse(compressed):
        compressed_tree = tree.Tree.fromstring(str(p))
        break

    #get labels and features
    features = get_features_recursive(original_tree, original.split(' '))
    labels = get_labels_recursive(original_tree, compressed_tree)
    return (features, labels)

if __name__ == '__main__':
    training_features = []
    training_labels = []

    if USE_BROADCAST:
        training_sentences = []
        for folder in os.listdir(BROADCAST_CORPUS_PATH):
            training_sentences += get_corpus_data(BROADCAST_CORPUS_PATH+folder)
        log_info("{0} sentences found".format(len(training_sentences)))
        for i in range(len(training_sentences)):
            if i >= MAX_SENTS:
                break
            log_info("processing sentence {0} of {1}".format(i, len(training_sentences)))
            feats, labels = extract_training_data(training_sentences[i])
            training_features += feats
            training_labels += labels
    if USE_WRITTEN:
        training_sentences = get_corpus_data(WRITTEN_CORPUS_PATH)
        log_info("{0} sentences found".format(len(training_sentences)))
        for i in range(len(training_sentences)):
            if i >= MAX_SENTS:
                break
            log_info("processing sentence {0} of {1}".format(i, len(training_sentences)))
            feats, labels = extract_training_data(training_sentences[i])
            training_features += feats
            training_labels += labels

    f = open('training_data', 'wb')
    pickle.dump((training_features, training_labels), f)
    f.close()

    model = LogisticRegression(solver='lbfgs', multi_class='auto').fit(training_features, training_labels)
    f = open('compression_model', 'wb')
    pickle.dump(model, f)
    f.close()
