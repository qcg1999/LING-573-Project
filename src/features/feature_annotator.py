from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

class EntityParser(object):
	def __init__(self):
		pass

	def __call__(self, sentence):
		tokens = [token for token in word_tokenize(sentence) if token.isalnum()]
		parsed = ne_chunk(pos_tag(tokens))
		return tree2conlltags(parsed)		
		

def annotate(sentences):
	parser = EntityParser()
	enriched = []
	for sentence in sentences:
		sentence = sentence[1].strip()
		parsed = parser(sentence)
		enriched += [parsed]
	return enriched
