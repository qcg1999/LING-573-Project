import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

def get_features(sentences):
    #first pass: get vocab and tokenize sentences
    processed_sentences = []
    vocab_dict = {}
    vocab_list = []
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

    return features

def dist(vector1, vector2, cosine):
    if cosine == 0:
        return np.linalg.norm(vector1 - vector2)
    else:
        return sum(vector1 * vector2) / (np.sqrt(sum(vector1*vector1)) * np.sqrt(sum(vector2 * vector2)))

def cost(vector_list):
    cost = 0
    for i in range(1, len(vector_list)):
        cost += dist(vector_list[i-1], vector_list[i], 1)
    return cost

def permutations(my_list):
    if len(my_list) <= 1:
        return [my_list]
    else:
        new_list = []
        for i in range(len(my_list)):
            sub_list = my_list[:i]+my_list[i+1:]
            for p in permutations(sub_list):
                new_list.append([my_list[i]] + p)
        return new_list

def ts_order(sentences):
    features = get_features(sentences)
    sentence_tuples = [(features[i], sentences[i]) for i in range(len(sentences))]

    #use brute force search
    best_cost = 1.0
    best_order = sentence_tuples.copy()
    for p in permutations(sentence_tuples):
        c = cost(np.array([i[0] for i in p]))
        if c < best_cost:
            best_cost = c
            best_order = p.copy()
    return [s[1] for s in best_order]
