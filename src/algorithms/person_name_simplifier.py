import spacy
import os

def simplify_names(sents):
	sents_new = []
	nlp = spacy.load('en')
	person = {}
	count = 0
	for s in sents:
#		print("\ns[{0}]:\n{1}".format(count, s))
		count += 1
		names_to_replace = []

		doc = nlp(s)
#		print("\nents:\n")
		for ent in doc.ents:
#			print(ent.text, ent.start_char, ent.end_char, ent.label_)
			if ent.label_ == 'PERSON':
				name_in_sent = ent.text
				name_in_token = name_in_sent.split()
#				print("\nnames: ", name_in_token) 
				if (len(name_in_token) > 1):
					if name_in_sent in person.keys():
#						print("full name reappeared.")
						names_to_replace.append(name_in_sent)
					else:
#						print("new full name.")
						person[name_in_sent] = name_in_token[-1]  #map to last name
			
		s_new = s
		if len(names_to_replace) >= 1:
			for name in names_to_replace:
				s_new = s_new.replace(name, person[name])

#		print("\ns_new: ", s_new)
		sents_new.append(s_new)
				
	return sents_new

if __name__ == '__main__':

	sents = [
		"Senior Palestinian official  Yasser Abed Rabbo denied on Tuesday reports saying that Palestinian leader Yasser Arafat has died in a French hospital."
		,
		"As Arafat had struggled for life, there has been wild guess as to where he might be buried and where to hold the funeral service."
		,
		"Sunday night, the French foreign minister, Michel Barnier, told LCI television that Arafat was alive but that his circumstances were complicated."
		,
		"Palestinian leader Yasser Arafat would be buried at his headquarters in the West Bank town of Ramallah, well-informed Palestinian sources said Tuesday."
	]

	sents_new = simplify_names(sents)

	print("\norig sents:")
	count = 0
	for s in sents:
		print("\ns[{0}]:\n{1}".format(count, s))
		count += 1
	
	print("\nnew sents:")
	count = 0
	for s in sents_new:
		print("\ns[{0}]:\n{1}".format(count, s))
		count += 1
		
