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

	positions = tree.treepositions()
	print("treepositions:", positions)

	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
			traverse_tree(subtree)	#recursive call

def get_position_and_flags(tree):
	position_flags = {}

	positions = tree.treepositions()

	# initialize
	for p in positions:
		position_flags[p] = 1	# 1: keep

	# apply rules here
	for p in positions:
		if position_flags[p] == 0:
			continue

		if type(tree[p]) == nltk.tree.Tree:
			#print ("label: ", tree1[p].label())
			label = tree[p].label()
			# remove PP
			if label == 'PP':
				position_flags[p] = 0   #0: not to keep
				#print("To be removed: \n", tree[p])
				# mark child node
				for p2 in positions:
					if is_leading(p, p2):
						position_flags[p2] = 0	
						#print("To be removed: \n", tree[p2])

	return positions, position_flags

def realize(tree, positions, position_flags):
	leaf_list = []

	for p in positions:
		if position_flags[p] == 0:		# not to keep
			continue
		if type(tree[p]) == str:
			leaf_list.append(tree[p])

	#print ("leaf_list: ", leaf_list)
	return " ".join(leaf_list) 

def is_leading(t1, t2):
	''' if t1 is a leading tuple of t2, return true.
	for example, if t1 = (1, 2), and t2 = (1, 2, 3)
	then, t1 is a leading tuple of t2.
	'''
	ret = True 

	if len(t1) > len(t2):
		return False 

	for i in range(0, len(t1)):
		if t1[i] != t2[i]:
			return False	

	return True


if __name__ == "__main__":

	# demonstration of usage

	#s = '(ROOT (S (NP (NNP Europe)) (VP (VBZ is) (PP (IN in) (NP (DT the) (JJ same) (NNS trends)))) (. .)))'
	#tree1 = tree.Tree.fromstring(s)
	s_1 = 'I came to Richmond in 1998'
	#s_1 = 'Senior Palestinian official Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital'

	print("sentence: ", s_1)

	parser = stanford.StanfordParser (
        model_path          = model_path,
        path_to_models_jar  = parser_jar
    )
	#parse
	s_parsed = parser.raw_parse(s_1)
	#form a tree
	for s in s_parsed:
		#print("s: ", s)
		print("s: ", str(s))
		tree1 = tree.Tree.fromstring(str(s))
		break
	
	#traverse_tree(tree1)

	'''
	# identify non-term nodes and term-node
	positions = tree1.treepositions()
	for p in positions:
		print ("\n")	
		print("p: ", p)
		print("tree1[p]:", tree1[p])
		print ("type: ",  type(tree1[p])) 
		if type(tree1[p]) == nltk.tree.Tree:
			print ("label: ", tree1[p].label())
		elif type(tree1[p]) == str:
			print ("leaf found: ",  tree1[p]) 
	'''
	
	positions, position_flags = get_position_and_flags(tree1)
	#print("position_flags: ", position_flags)
	#print("position_flags:\n", ["{0}: {1}\n".format(k, v) for k, v in position_flags.items()])
	#for k, v in position_flags.items():
	#	print("{1}: {0}".format(k, v))

	compressed = realize(tree1, positions, position_flags)
	print ("compressed: ", compressed)

	'''
	t1 = (1, 2, 3)
	t2 = (1, 2, 3, 4)
	t3 = (2, 2, 3, 4)
	lead = is_leading(t1, t2)
	#print ("lead: ", lead) 
	lead = is_leading(t1, t3)
	#print ("lead: ", lead) 
	'''

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
