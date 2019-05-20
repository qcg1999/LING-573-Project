#!/usr/bin/env python
import algorithms.entity_grid as grid 
import os
import unittest

class entity_grid_test(unittest.TestCase):
#	def __init__(self):
    
	def test_one_file_from_text_rank_full_list(self):
		#open generated files in outputs_full_text_rank; break them into sentence strings; call 
		#entity_grid method to genrated re-ordered senteces
		#sents_file = '../../outputs_full_text_rank/D0901-A.M.100.A.0'
		sents_file = '../../outputs_full_text_rank/D0918-A.M.100.D.0'
		sents = []
		with open(sents_file) as f:
			for line in f:
				line = line.rstrip()
				if len(line) == 0:
					continue
				sents.append(line)

		f.close()
		print("before: number of sentences: {0}".format(len(sents)))

		#call entity-grid based ordering logic
		try:
			sents = grid.get_ordered_sentences(sents[0:10])
		except UnicodeDecodeError:
			print("UnicodeDecodeError")
		else:
			print("Error occured at grid.get_ordered_sentences")

		print("after: number of sentences: {0}".format(len(sents)))

		#show the first 10 sentences
		count = 0
		print("ordered sentences: \n")
		for s in sents:
			print(s)
			count += 1
			if count >= 10:
				break

		self.assertEqual(1, 1)

	def test_all_files_from_text_rank_full_list(self):
		#get all files from ../../outputs_full_text_rank
		
		sents_file_folder = '../../outputs_full_text_rank'
		sents_files = []
		for f in os.listdir(sents_file_folder):
			sents_files.append(f)

		#print(sents_files)
		for fname in sents_files:
			sents = []
			with open(sents_file_folder + "/" + fname) as f:
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
				sents = grid.get_ordered_sentences(sents[0:10])
			except UnicodeDecodeError:
				print("UnicodeDecodeError")
			else:
				print("")

			print("after: number of sentences: {0}".format(len(sents)))
			#show the first 10 sentences
			count = 0
			print("ordered sentences: \n")
			for s in sents:
				print(s)
				count += 1
				if count >= 10:
					break
				


		self.assertEqual(1, 1)
        
        
if __name__ == '__main__':
    unittest.main()
