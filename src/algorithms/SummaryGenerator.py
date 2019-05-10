#!/usr/bin/env python
class SummaryGenerator:
    "Generates summary given various input data and associated models"
    
    def __init__(self):
        pass
    
    #def __init__(self, sentenceList):
    #    self.sentenceList = sentenseList
        
    def Import(self, inputFile):
        pass
    
    def ToSummary(self, listOfWords = None):
        """returns a string (concatenated) words of the first 100 elements in input list"""
        if listOfWords is not None:
            summaryWords = listOfWords[:100]
            return " ".join(summaryWords)       # a string to words
        
    
    #def ToSummary(self):
    #    """generates a summary out to console (standard output) """
    #    return "a summary"
        
    def SentenceCount(self):
        """returns number of sentences"""
        return 0
        
    def WordCount(self):
        """returns number of words"""
        return 0
    

