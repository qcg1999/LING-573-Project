from nltk.parse import stanford
import os

if __name__ == "__main__":


	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'

	os.environ['CLASSPATH'] = stanford_home
	
	sentences = [
		"It was a rainy day.",
		"Bob returned a book to the library.", 
		"The book was over due.", 
		"Bob was not happy.", 
	]

	parser = stanford.StanfordParser(
		model_path			=model_path, 
		path_to_models_jar	=parser_jar
	)

	#syntax parser
	sent = "I came to Richmond in 1998."
	print ("sent:", sent)
	parse_tree = parser.raw_parse(sent)
	for t in parse_tree:
		print("syntax parse tree\n", t)

	#parse multiple sentence
	for s in sentences:
		print("sent: ", s)
	parse_trees = parser.raw_parse_sents(sentences, verbose=True)
	for ps_list in parse_trees:
		for ps in ps_list:
			print("syntax parse tree:\n", ps)

	'''	
	dep_parser = stanford.StanfordDependencyParser(
		model_path			=model_path, 
		path_to_models_jar	=parser_jar
	)

	parse_tree = dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")

	print("parse_tree:\n", parse_tree) 
	'''
#eof
