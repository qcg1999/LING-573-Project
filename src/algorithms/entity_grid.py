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
		for s in sentences:
			try:
				#s = bytes(s,'utf-8').decode('utf-8', 'ignore')
				s = s.replace('é', 'e')
				results += [self._execute(cmd, s, verbose)]
			except:
				print("raw_parse_sents error on sentence: {0}".format(s))
				continue
			
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
	parser = Parser(stanford_home, model_path, parser_jar)
	enriched_sentences, entities = parser(sentences)

	#print(enriched_sentences)
	#print(entities)

	grid = _order_entity_grid(enriched_sentences, entities)
	return grid

def get_ordered_sents_indices_1(grid):
	''' given an entity grid with rows being sentence index and columns being entities; 
		argument grid is of DataFrame type in package of Pandas
	'''
	row_indices = []  # a list of sentence index re-ordered by this method 

	row_num = grid.shape[0] # total number of rows
	weight = {}  # a dictionary of calculated weight of entities 
	column_list = list(grid.columns.values)
	#loop through each column, and find one with the larget value
	while len(row_indices) < row_num:	
		remaining_rows = [x for x in range(row_num) if x not in row_indices]
		#r_selected = max(remaining_rows) 
		#(re)calc weights
		for col in column_list:
			weight[col] = 0  #(re)initialize
			for row in remaining_rows:
				weight[col] += grid.at[row, col]
		#print("weight:\n", weight)

		#find column with the highest weight
		import operator
		c_selected = max(weight.items(), key=operator.itemgetter(1))[0]
		#print("entity selected: ", {k:v for k, v in weight.items() if k in c_selected})

		#find a sentence (row) with the highest weight on this column (entity)
		r_selected = -1 
		w_selected = 0
		for row in remaining_rows:
			if grid.at[row, c_selected] > w_selected:
				r_selected = row	
				w_selected = grid.at[row, c_selected]
		

		if r_selected >= 0:
			row_indices.append(r_selected)
	
	#print("sents_indices: \n", row_indices)
	return row_indices

def get_ordered_sents_indices(grid):
	''' given an entity grid with rows being sentence index and columns being entities; 
		argument grid is of DataFrame type in package of Pandas
	'''
	row_indices = []  # a list of sentence index re-ordered by this method 

	row_num = grid.shape[0] # total number of rows
	weight = {}  # a dictionary of calculated weight of entities 
	column_list = list(grid.columns.values)
	column_mentioned = []  # saves entities mentioned in selected rows
	#loop through each column, and find one with the larget value
	while len(row_indices) < row_num:	
		#print("\n")
		remaining_rows = [x for x in range(row_num) if x not in row_indices]
		#r_selected = max(remaining_rows) 

		#(re)calc weights for each column (entity) over remaining rows (sentences)
		for col in column_list:
			weight[col] = 0  #(re)initialize
			for row in remaining_rows:
				weight[col] += grid.at[row, col]
		#print("weights:\n", weight)

		#find column with the highest weight
		import operator
		c_selected = max(weight.items(), key=operator.itemgetter(1))[0]

		#break ties on column(entity) selected
		weight_max = max(weight.items(), key=operator.itemgetter(1))[1]
		#print("weight_max: ", weight_max)
		#find all colmns with max weight
		col_candidates = []
		for col in column_list:
			if weight[col] == weight_max:
				col_candidates.append(col)

		#print("col_candidates:\n", col_candidates)	
		#print("column_mentioned:\n", column_mentioned)	
		#pick one from candidates
		# by preceeding one
		filtered_by_column_mentioned = []
		if len(col_candidates) > 1:
			filtered_by_column_mentioned = [c for c in col_candidates if c in column_mentioned]
			#print("filtered_by_column_mentioned:\n", filtered_by_column_mentioned)

		if len(filtered_by_column_mentioned) >= 1:
			col_candidates = filtered_by_column_mentioned
		
		
		# by POS-Subject (S)
		# among all remaining rows (sentencies), which column (entity) is maximuly mentioned as a subject (S) 
		'''
		filtered_by_subject = []
		subject_weight = {}
		if len(col_candidates) > 1:
			for col in column_list:
				subject_weight[col] = 0
				for row in remaining_rows:
					if grid.at[row, col] == 1.0:
						subject_weight[col] += grid.at[row, col]

		print("subject_weight:\n", subject_weight)
		'''
		# by POS-Object (O)
		# by POS-Others (X)

		# by original order (default)
		c_selected = col_candidates[0]
		#print("c_selected: ", c_selected)

		#find a sentence (row) with the highest weight on this column (entity)
		r_selected = -1  #to be determined
		w_selected = 0  #weight at row-level in the selected column
		for row in remaining_rows:
			if grid.at[row, c_selected] > w_selected:
				w_selected = grid.at[row, c_selected]

		# Find all matched rows (sent) that matches this weight 
		candidate_rows = []
		for row in remaining_rows:
			if grid.at[row, c_selected] == w_selected:
				candidate_rows.append(row)

		#print("candidate_rows: \n", candidate_rows)

		# more ordering logic to be added here
		# default to the first among the original order
		r_selected = candidate_rows[0]
		#print("row selected: ", r_selected)

		if r_selected >= 0:
			row_indices.append(r_selected)

			#Add all (S, O, X) in the selected row (sentence) to the mentioned colunm (entity) list
			c_mentioned = []  #column (entity) mentioned in this row (sentence)
			for col in column_list:
				if grid.at[r_selected, col] > 0:
					c_mentioned.append(col)		  #add to row(sentence-level) mentioned column(entity) list
			
			for col in c_mentioned:
				if col not in  column_mentioned:
					column_mentioned.append(col)  #add to overall mentioned column (entity) list
	
	#print("sents_indices: \n", row_indices)
	return row_indices


def get_ordered_indices(sentences):

	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

	grid = order_entity_grid(sentences, stanford_home, model_path, parser_jar)
	#print(grid)
	indices =  get_ordered_sents_indices(grid)
		
	print("index of reordered sents: \n", indices)

	return indices

def get_ordered_sentences(sentences):

	indices = get_ordered_indices(sentences)

	sents = [sentences[i] for i in indices]

	return sents 

if __name__ == "__main__":


	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'
	
#	sentences = ["Bob gave Alice a pizza.", 
#				"Alice was happy with Jim."]

	sentences = [
		"It was a rainy day",
		"Bob returned a book to the library", 
		"The book was over due", 
		"Bob was not happy", 
	]

	#grid = order_entity_grid(sentences, stanford_home, model_path, parser_jar)
	#print(grid)

	print("input sentences: \n", sentences)

	sents =  get_ordered_sentences(sentences)

	print("reordered sentences: \n", sents)

#eof
