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

def _order_entity_grid(sentences, entities, subj_rank=1.0, obj_rank=0.5, other_rank=0.1):
	grid = make_grid(sentences, entities)
	for index, (sentence, relations) in enumerate(sentences):
		for entity,rel in relations.items():
			if 'subj' in rel:
				grid.at[index,entity] = subj_rank
			elif 'obj' in rel:
				grid.at[index,entity] = obj_rank
			else:
				grid.at[index,entity] = other_rank

	print("grid in _order_entity_grid:\n", grid)

	return grid

def order_entity_grid(sentences, stanford_home, model_path, parser_jar):
	#sentences = [tup[1] for tup in sentence_tuples]
	#sentences = [tup[1] for tup in sentence_tuples]
	parser = Parser(stanford_home, model_path, parser_jar)
	enriched_sentences, entities = parser(sentences)

	print(enriched_sentences)
	print(entities)

	grid = _order_entity_grid(enriched_sentences, entities)
	return grid

def get_ordered_sents_index(grid):
	''' given an entity grid with rows being sentence index and columns being entities; 
		argument grid is of DataFrame type in package of Pandas
	'''
	index = []  # a list of sentence index re-ordered by this method 

	weight = {}  # a dictionary of calculated weight of entities 
	for c in grid.columns:
		weight[c] = sum(grid[c])

	#print("weight: \n", weight)
	entity_names = weight.keys();

	accounted = [] # saves entities accounted for
	#loop through each column, and find one with the larget value
	while len(accounted) < len(entity_names):

		remained = {k:v for k, v in weight.items() if k not in accounted}
		#print("remained:",remained)

		#get the entity with the maximum weight
		import operator
		selected = max(remained.items(), key=operator.itemgetter(1))[0]
		#print("selected: ", {k:v for k, v in weight.items() if k in selected})

		accounted.append(selected)
		#print("accounted: ", accounted)

		#select sentences associcated with this entity
		sents_selected = grid[selected][grid[selected] > 0]
		# sort by weight in sentences
		# may consider other factors such as POS (S and O, for example)
		sents_selected = sents_selected.sort_values(ascending=False)

		# get sents index
		sents_index = list(sents_selected.keys())
		#print("setence_selected:\n", sents_index)

		#index.append(sents_index)
		index += [e for e in sents_index if e not in index]

		#you could update weight here

	return index

def get_ordered_index(sentences):

	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

	grid = order_entity_grid(sentences, stanford_home, model_path, parser_jar)
	#print(grid)
	try: 
		index =  get_ordered_sents_index(grid)
	except UnicodeDecodeError:
		print("UnicodeDecodeError occured")
	else:
		print("")
		
	#index = [i for i in range(0, len(sentences))]
	print("index of reordered sents: \n", index)

	return index

def get_ordered_sentences(sentences):

	index = get_ordered_index(sentences)

	sents = [sentences[i] for i in index]

	return sents 

if __name__ == "__main__":

	#import pdb; pdb.set_trace()

	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'
	
#	sentences = ["Bob gave Alice a pizza.", 
#				"Alice was happy with Jim."]

	sentences = ["Bob returned a book to the library", "The book was over due", 
				"Bob was not happy.", "It was a rainy day"]

	#parser = Parser(stanford_home, model_path, parser_jar)
	#sentences, entities = parser(sentences)

	grid = order_entity_grid(sentences, stanford_home, model_path, parser_jar)
	#print(grid)
	index =  get_ordered_sents_index(grid)
	print("index: ", index)

	print("sentence ordered: \n")
	for i in index:
		print("{0}\n".format(sentences[i]))

#eof
