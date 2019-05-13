from bs4 import BeautifulSoup
import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np

def get_features(docs):
    sentences = []
    positions = []

    vocab_dict = {}
    vocab_list = []

    tokenizer = RegexpTokenizer(r'\w+')

    #trivial system: just get first paragraph of first document
#    file_name, file_id = docs[0]
#    f = open(file_name)
#    soup = BeautifulSoup(f.read(), "lxml")
#    return soup.find("doc", id=file_id).find('p').text.split()

    for file_name, file_id in docs:
        f = open(file_name)
        soup = BeautifulSoup(f.read(), "lxml")
        docs = soup.findAll("doc", id=file_id)
        for doc in docs:

            #get sentences and positions in document
            doc_sentences = []
            doc_positions = []
            for p in doc.findAll("p"):
                doc_sentences += nltk.sent_tokenize(p.text)
            n = len(doc_sentences)
            for i in range(n):
                doc_positions.append(float(i)/n)

            sentences += doc_sentences
            positions += doc_positions

    #first pass: get vocab and tokenize sentences
    processed_sentences = []
    stop_words = stopwords.words('english')
    for sent in sentences:
        sent_array = []
        for word in tokenizer.tokenize(sent):
            word = word.lower()
            if not word in stop_words:
                sent_array.append(word)
                if not word in vocab_dict:
                    vocab_dict[word] = len(vocab_list)
                    vocab_list.append(word)
        processed_sentences.append(sent_array)

    features = np.zeros((len(sentences), len(vocab_list)))

    #second pass: fill feature matrix
    for i in range(len(processed_sentences)):
        for word in processed_sentences[i]:
            features[i, vocab_dict[word]] += 1

    return [(positions[i], sentences[i]) for i in range(len(sentences))], features
