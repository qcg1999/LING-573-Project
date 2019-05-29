import nltk
from nltk import tree
from nltk.parse import stanford
import os

stanford_home 	= '/NLP_TOOLS/parsers/stanford_parser/latest/'
model_path 		= '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
parser_jar 		= '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

os.environ['CLASSPATH'] = stanford_home

def compress(sentences):

	return sentences

def traverse_tree(tree):
	print("lable: ", tree.label())
	#print("type(tree):", type(tree))

	#positions = tree.treepositions()
	#print("treepositions:", positions)

	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
			traverse_tree(subtree)

def get_position_and_flags(tree):
	position_flags = {}

	positions = tree.treepositions()

	# initialize
	for p in positions:
		position_flags[p] = 1	# 1: keep; #0: not to keep

	# apply rules here
	for p in positions:
		#print("\ntype(tree[p]): ", type(tree[p]))	
		if type(tree[p]) == str:
			continue
		else:
			label = tree[p].label()
			print("label: ", label)	
			if label == 'PP':
				position_flags[p] = 0   #do not keep


	return positions, position_flags

def realize(tree, positions, position_flags):
	leaf_list = []

	for p in positions:
		if position_flags[p] == 0:		# not to keep
			continue
		if type(tree[p]) == str:
			leaf_list.append(tree[p])
		
	'''
	for k in position_flags.keys():
		if type(tree[k]) == str:
			print ("leaf found: ",  tree[k]) 
			leaf_list.append(tree[k])
	'''


	print ("leaf_list: ", leaf_list)
	return leaf_list


if __name__ == "__main__":

	# demonstration of usage

	#s = '(ROOT (S (NP (NNP Europe)) (VP (VBZ is) (PP (IN in) (NP (DT the) (JJ same) (NNS trends)))) (. .)))'
	#tree1 = tree.Tree.fromstring(s)
	s_1 = 'Senior Palestinian official Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital'

	parser = stanford.StanfordParser(
        model_path          =model_path,
        path_to_models_jar  =parser_jar
    )

	s_parsed = parser.raw_parse(s_1)

	for s in s_parsed:
		#print("s: ", s)
		print("s: ", str(s))
		tree1 = tree.Tree.fromstring(str(s))
		break
	
	#traverse_tree(tree1)


	#positions = tree1.treepositions()
	'''
	for p in positions:
		#print ("\n")	
		#print("p: ", p)
		#print("tree1[p]:", tree1[p])
		#print ("type: ",  type(tree1[p])) 
		if type(tree1[p]) == str:
			print ("leaf found: ",  tree1[p]) 
	'''
	
	positions, position_flags = get_position_and_flags(tree1)
	print("position_flags: ", position_flags)

	realize(tree1, positions, position_flags)

	'''
	sentences_list_01 = [
		"It was a rainy day",
		"Bob returned a book to the library", 
		"The book was over due", 
		"Bob was not happy", 
	]

	sentences_list_02 = [
		"Senior Palestinian official Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital",
		"As Arafat had struggled for life, there has been wild guess as to where he might be buried and where to hold the funeral service",
		"Sunday night the French foreign minister, Michel Barnier, told LCI television that Arafat was alive but that his circumstances were complicated"
		"Sunday night, the French foreign minister, Michel Barnier, told LCI television that Arafat was alive but that his circumstances were complicated"
	]

	compressed = compress(sentences_list_02);

	print("compressed:\n", compressed)

	'''

#eof
