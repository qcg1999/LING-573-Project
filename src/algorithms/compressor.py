import pandas as pd
import numpy as np
import os
import pprint


def compress(sentences):

	return sentences


if __name__ == "__main__":

	# demonstration of usage

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

#eof
