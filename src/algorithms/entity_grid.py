from nltk.parse.stanford import GenericStanfordParser
import pandas as pd
import numpy as np
import os

class DependencyParser(GenericStanfordParser):
	_OUTPUT_FORMAT = 'typedDependencies'
	_ENTITY_RELS = ["subj", "obj", "prep_with"]
	def __init__(self, *args, **kwargs):
		super(DependencyParser,self).__init__(*args,**kwargs)

	def raw_parse_sents(self, sentences, verbose=False):
		results = []
		cmd = [
			self._MAIN_CLASS,
			'-outputFormat',
			self._OUTPUT_FORMAT,
			self.model_path,
			"-sentences",
			"newline",
		]
		for sentence in sentences:
			results += [self._execute(cmd, sentence, verbose)]
			
		return self._prepare_output(sentences, results)

	def _prepare_output(self, sentences, result):
		assert len(result) == len(sentences), "Sentence/result mismatch"
		parsed = zip(sentences, result)
		total_entities = set()
		sentences_and_entities = []
		for sentence, relations in parsed:
			entities = dict()
			for deprel in relations.split('\n'):
				deprel = deprel.strip()
				if not deprel: continue
				relation_func = deprel.split("(")
				relation = relation_func[0]
				token = deprel.split()[1].split("-")[0]
				if any(rel in relation for rel in self._ENTITY_RELS):
					entities[token] = relation
			total_entities.update(entities.keys())
			sentences_and_entities += [(sentence, entities)]
		return sentences_and_entities, total_entities

class Parser(object):
	def __init__(self, stanford_home, model_path, parser_jar):
		os.environ['CLASSPATH'] = stanford_home
		self._parser = DependencyParser(model_path=model_path, 
							path_to_models_jar=parser_jar)
		
	def __call__(self, sentences):
		return self._parser.raw_parse_sents(sentences)

def make_grid(rows, columns):
	grid = pd.DataFrame(index=np.arange(len(rows)), columns=columns,dtype=np.float32)
	grid = grid.fillna(0)
	return grid	

def _entity_grid_order(sentences, entities, subj_rank=1.0, obj_rank=0.5, other_rank=0.1):
	grid = make_grid(sentences, entities)
	for index, (sentence, relations) in enumerate(sentences):
		for entity,rel in relations.items():
			if 'subj' in rel:
				grid.at[index,entity] = subj_rank
			elif 'obj' in rel:
				grid.at[index,entity] = obj_rank
			else:
				grid.at[index,entity] = other_rank
	#print(grid)
	# do stuff with grid

def entity_grid_order(sentence_tuples, args):
	sentences = [tup[1] for tup in sentence_tuples]
	parser = Parser(args.stanford_home, args.model_path, args.parser_jar)
	enriched_sentences, entities = parser(sentences)
	_entity_grid_order(enriched_sentences, entities)

if __name__ == "__main__":
	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'
	
	sentences = ["Bob gave Alice a pizza.", "Alice was happy with Jim."]
	parser = Parser(stanford_home, model_path, parser_jar)

	sentences, entities = parser(sentences)
	_entity_grid_order(sentences, entities)
