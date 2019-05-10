import spacy

class SpacyParser(object):
	def __init__(self, model='en'):
		self._parser = spacy.load(model)
	
	@property
	def parser(self):
		return self._parser

	def parse(self, text):
		return [(t.text, t.tag_, "%s-%s" % (t.ent_iob_, t.ent_type_)) for t in self._parser(text)]

def annotate(sentences):
	parser = SpacyParser()
	enriched = []
	for sentence in sentences:
		sentence = sentence[1].strip()
		parsed = parser.parse(sentence)
		enriched += [parsed]
	return enriched
