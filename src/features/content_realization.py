'''Utilities for cleaning result sentences
'''


def realize(ranked_sentence_tuples, max_words=100):
	summary = ''
	for sentence_tuple in ranked_sentence_tuples:
		sentence = _clean(sentence_tuple[1])
		summary = '%s\n%s' % (summary,sentence)
	return summary.strip()

def cut_off(ranked_sentence_tuples, max_words=100):
	summary_sentences = []
	summary = ""
	for sentence_tuple in ranked_sentence_tuples:
		sentence = _clean(sentence_tuple[1])
		summary = '%s\n%s' % (summary,sentence)
		if len(summary.split()) > max_words:
			break
		summary_sentences.append(sentence_tuple)
	return summary_sentences
	

def _clean(sentence):
	sentence = sentence.replace('\n',' ').strip()
	return sentence
