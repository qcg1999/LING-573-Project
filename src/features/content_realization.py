'''Utilities for cleaning result sentences
'''


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
	return sentence
