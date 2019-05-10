#!/usr/bin/env python
import SummaryGenerator
import unittest
from nltk.corpus import brown

class SummaryGeneratorTester(unittest.TestCase):
    #def __init__(self):
    
    def testCount(self):
        sg = SummaryGenerator.SummaryGenerator()
        words = ["one", "two", "three", "four"]
        summary = sg.ToSummary(words)
        self.assertEqual(len(summary.split()), 4)
        
        
        summary = sg.ToSummary(brown.words(categories='news'))
        self.assertEqual(len(summary.split()), 100)
        
        
if __name__ == '__main__':
    unittest.main()
