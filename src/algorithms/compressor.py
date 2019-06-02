import nltk
from nltk import tree
from nltk.parse import stanford
import os
import string

stanford_home 	= '/NLP_TOOLS/parsers/stanford_parser/latest/'
model_path 		= '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
parser_jar 		= '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

os.environ['CLASSPATH'] = stanford_home

def compress_sents(sentences):
	''' compress a list of sentences
	'''
	compressed = []
	for s in sentences:
		c = compress_sent(s)
		compressed.append(c)
		#stop at 100 words
		if len((' '.join(compressed)).split(' ')) > 100:
			break

	return compressed

def compress_sent(sent):
	sent = compress_sent_tree(sent)
	return sent

def compress_sent_tree(sentence):
	''' compress a given sentence (as a string of words)
		return a compressed sentence (also as a string of words)
	'''	
	print("\ncompressing sentence: ", sentence)

	parser = stanford.StanfordParser (
        model_path          = model_path,
        path_to_models_jar  = parser_jar
    )
	
	try:
		#parse
		s_parsed = parser.raw_parse(sentence)
		#form a tree
		for s in s_parsed:
			#print("parse: ", str(s))
			tree1 = tree.Tree.fromstring(str(s))
			break
	
		positions, position_flags = get_position_and_flags(tree1)
		#for k, v in position_flags.items():
		#	print("{1}: {0}".format(k, v))

		compressed = realize(tree1, positions, position_flags)
	except:
		print("\nno compression performed duo to an error in parse. sentence: {0} \n".format(sentence))
		compressed = sentence
		
	#print ("compressed: ", compressed)

	return compressed

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
		if position_flags[p] == 0:  #already visited and set false to keep
			continue

		if type(tree[p]) == nltk.tree.Tree:		# non-term node
			#print ("label: ", tree1[p].label())
			label = tree[p].label()

			# rules:
			# remove PP
			if label == 'PP':
				#print("PP identified.")
				#position_flags[p] = 0   #0: not to keep
				#print("To be removed: \n", tree[p])
				# mark 'flase' to keep on all child nodes
				'''
				for p2 in positions:
					if is_leading(p, p2):  # is a child node
						position_flags[p2] = 0	
						#print("To be removed: \n", tree[p2])
				'''
				children = find_child_positions(p, positions)
				#print("# children: ", len(children))
				# mark to remove
				if len(children) <= 15:
					position_flags[p] = 0   #0: not to keep
					#print("To be removed: \n", tree[p])
					for c in children:
						position_flags[c] = 0
						#print("To be removed: \n", tree[c])

			# other rules
			elif label == 'DT':  # determiner 'the, The'
				position_flags[p] = 0   #0: not to keep
				children = find_child_positions(p, positions)
				for c in children:
					position_flags[c] = 0
				

		elif type(tree[p]) == str:	# term node
			# rules on term node
			continue

	return positions, position_flags

def find_child_positions(pos, positions):
	''' find all child postions in 'positions' for a given position 'pos'
	'''
	child_positions = []
	for p in positions:
		if is_leading(pos, p):
			child_positions.append(p)

	return child_positions


def realize(tree, positions, position_flags):
	leaf_list = []

	for p in positions:
		if position_flags[p] == 0:		# not to keep
			continue
		if type(tree[p]) == str:
			leaf_list.append(tree[p])

	sent = " ".join(leaf_list)

	#remove space before a punctuation
	if (len(sent) >= 1):
		for p in string.punctuation:
			sent = sent.replace(' ' + p, p)

	#strip off leading punctuation
	if (len(sent) >= 1):
		if sent[0] in string.punctuation:
			sent = sent[1:]

	#strip off leading space
	if (len(sent) >= 1):
		if sent[0] == ' ':
			sent = sent[1:]
	
	return sent 

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
	#s_1 = 'Europe is in the same trends'
	s_1 = 'I live in Greater Richmond since 1998'
	#s_1 = 'Senior Palestinian official Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital'


	print("input sentence: ", s_1)
	compressed_sent = compress_sent(s_1)
	print("compressed: ", compressed_sent)

	sentences_list_02 = [
		"Senior Palestinian official Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital",
		"As Arafat had struggled for life, there has been wild guess as to where he might be buried and where to hold the funeral service",
		"Sunday night, the French foreign minister, Michel Barnier, told LCI television that Arafat was alive but that his circumstances were complicated",
		"Palestinian leader Yasser Arafat would be buried at his headquarters in the West Bank town of Ramallah, well-informed Palestinian sources said Tuesday"
	]
	'''
	for s in sentences_list_02:
		print("\n")
		print("input sentence: ", s)
		compressed = compress_sent(s)
		print("compressed:     ", compressed) 
	'''

	compressed_list_02 = compress_sents(sentences_list_02)
	for s in compressed_list_02:
		print("\n")
		
		print("compressed:     ", s)

#eof
