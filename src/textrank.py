import numpy.linalg as la
import numpy as np
import networkx as nx


def textrank(feature_matrix,src_matrix):
	'''TextRank algorithm
		given an NxM feature matrix, generate a similarity matrix using cosine similarity and
		execute standard PageRank algorithm. Returns a sorted set of sentences.
	'''
	ranked = _textrank(feature_matrix)
	ranked = sorted(((ranked[i],s) for i,s in enumerate(src_matrix)), reverse=True)
	return ranked

def _fast_pairwise_cosine_distance(matrix):
	base_sims = np.dot(matrix,matrix.T).astype(np.float32)
	inverse_square_magnitude = 1 / np.diag(base_sims)
	inverse_square_magnitude[np.isinf(inverse_square_magnitude)] = 0
	inverse_magnitude = np.sqrt(inverse_square_magnitude)
	return np.array(base_sims * inverse_magnitude).T * inverse_magnitude

def _textrank(feature_matrix):
	similarities = _fast_pairwise_cosine_distance(feature_matrix)
	return nx.pagerank(nx.from_numpy_array(similarities))


if __name__ == "__main__":
	'''Demo use case
	'''
	import nltk
	import pandas as pd
	from sklearn.metrics import pairwise_distances
	from sklearn.feature_extraction.text import CountVectorizer

	corpus = [' '.join(s) for s in nltk.corpus.brown.sents(categories='news')][100:200]
	vocab = set(nltk.corpus.brown.words(categories='news'))

	vectorizer = CountVectorizer(vocabulary=vocab)
	df = pd.DataFrame(data=corpus,columns=['sentences'])
	feats = vectorizer.fit_transform(df['sentences'].values)

	feats = np.array(feats.toarray(),dtype=np.int32)

	ranked = textrank(feats, corpus, len(vocab))
	for sent in ranked[0:5]:
		print sent
