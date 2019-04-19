from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np

def get_features(docs):
    sentences = []

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
            for p in doc.findAll("p"):
                sentences += nltk.sent_tokenize(p.text)

    #first pass: get vocab 
    for sent in sentences:
        for word in tokenizer.tokenize(sent):
            word = word.lower()
            if not word in stopwords.words('english'):
                if not word in vocab_dict:
                    vocab_dict[word] = len(vocab_list)
                    vocab_list.append(word)

    features = np.zeros((len(sentences), len(vocab_list)))

    #second pass: fill feature matrix
    for i in range(len(sentences)):
        for word in tokenizer.tokenize(sentences[i]):
            word = word.lower()
            if not word in stopwords.words('english'):
                word = word.lower()
                features[i, vocab_dict[word]] += 1

    return sentences, features
