import algorithms.entity_grid as grid 
import algorithms.compressor as compressor
from features.content_realization import *
import os
import unittest

TRUNC_SIZE = 2 

class compressor_test(unittest.TestCase):
	def print_sents(self, sents):
		count = 0
		for s in sents:
			print("\ns[{0}]: {1}".format(count, s))
			count += 1
			if count > TRUNC_SIZE:
				break

#	def __init__(self):
    
	def test_one_file_from_text_rank_full_list(self):
		#open generated files in outputs_full_text_rank; break them into sentence strings; call 
		#entity_grid method to genrated re-ordered senteces
		#input_file = '../../outputs_full_text_rank/D0901-A.M.100.A.0'

		input_file_folder = '../../outputs_full_text_rank/'
		output_file_folder = '../../outputs/'

		input_file = 'D0918-A.M.100.D.0'
		sents = []
		with open(input_file_folder + input_file) as f:
			for line in f:
				line = line.rstrip()
				if len(line) == 0:
					continue
				sents.append(line)

		f.close()
		print("before: number of sentences: {0}".format(len(sents)))

		#call entity-grid based ordering logic
		try:
			sents = grid.get_ordered_sentences(sents[0:TRUNC_SIZE])
		except UnicodeDecodeError:
			print("UnicodeDecodeError")
		else:
			print("")

		print("\nordered sentences:")
		self.print_sents(sents)

		# compress sentences
		sents = compressor.compress_sents(sents)

		print("\ncompressed sentences:")
		self.print_sents(sents)

		summary = realize2(sents)
		print("\nsummary: \n", summary)

		summary_file = input_file

		print("\nsummary file {0}\n".format(summary_file) )

		f = open(output_file_folder + summary_file, "w+")
		f.write(summary)
		f.close()
		

		self.assertEqual(1, 1)

	def test_all_files_from_text_rank_full_list(self):
		#get all files from ../../outputs_full_text_rank
		
		input_file_folder = '../../outputs_full_text_rank'
		input_files = []
		for f in os.listdir(input_file_folder):
			input_files.append(f)

		#print(input_files)
		for fname in input_files:
			sents = []
			with open(input_file_folder + "/" + fname) as f:
				for line in f:
					line = line.rstrip()
					if len(line) == 0:
						continue
					sents.append(line)
			f.close()
			print("processing file {0}".format(fname))
			print("before: number of sentences: {0}".format(len(sents)))
			#call entity-grid based ordering logic
			try:
				sents = grid.get_ordered_sentences(sents[0:TRUNC_SIZE])
			except UnicodeDecodeError:
				print("UnicodeDecodeError")
			else:
				print("")

			
			#show the first 10 sentences
			print("\nordered sentences: \n")
			self.print_sents(sents)

			# compress sentences
			print("\ncompressed sentences: \n")
			self.print_sents(sents)

			#show the first 10 sentences
			print("\n")
			print("compressed sentences: \n")
			self.print_sents(sents)

		self.assertEqual(1, 1)
        
if __name__ == '__main__':
    unittest.main()
