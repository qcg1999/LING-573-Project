'''Utilities for cleaning result sentences
'''
import re

def truncate(ranked_sentences, max_words=100):
	summary_sentences = []
	summary = ""
	for sentence in ranked_sentences:
		sentence = _clean(sentence)
		summary = "%s\n%s" % (summary, sentence)
		if len(summary.split()) > max_words:
			break
		summary_sentences.append(sentence)
	return summary_sentences

def realize2(sentences, max_words=100):
	summary = ''
	len_summary = 0
	for s in sentences:
		s = _clean(s)
		len_s = len(s.split())
		if len_summary + len_s >  max_words:
			break
		summary = '%s\n%s' % (summary, s)
		len_summary += len_s
	return summary.strip()	

def realize(ranked_sentence_tuples, max_words=100):
	summary = ''
	for sentence_tuple in ranked_sentence_tuples:
		sentence = _clean(sentence_tuple[1])
		if len(('%s %s' % (summary,sentence)).split()) > max_words:
			break
		summary = '%s\n%s' % (summary,sentence)
	return summary.strip()	

def _clean(sentence):
	sentence = sentence.replace('\n',' ').strip()
	#fix punctuation
	sentence = re.sub(r'\s([?.!,\'])', r'\1', sentence)
	sentence = re.sub(r'(\$)\s', r'\1', sentence)
	#Capitalize
	sentence = sentence[0].upper() + sentence[1:]
	return sentence
