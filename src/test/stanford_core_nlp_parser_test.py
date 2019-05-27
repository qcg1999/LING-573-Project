from nltk.parse.corenlp import CoreNLPParser
import os


if __name__ == "__main__":


	stanford_home = '/NLP_TOOLS/parsers/stanford_parser/latest/'
	model_path = '/NLP_TOOLS/parsers/stanford_parser/latest/englishPCFG.ser.gz'
	parser_jar = '/NLP_TOOLS/parsers/stanford_parser/latest/stanford-parser.jar'
	
	os.environ['CLASSPATH'] = stanford_home

	parser = CoreNLParser(model_path=model_path, path_to_models_jar=parser_jar)
	parsed_sent = parser.raw_parse("I came to Richmond in 1998.")
	for ps in parsed_sent:
		print("ps:\n", ps)

#eof
