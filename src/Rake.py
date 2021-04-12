import operator
from typing import List, Tuple, Optional
import os
import jieba
import jieba.posseg as pseg
from .word import Word
from .utils import notNumStr

class Rake:

    def __init__(self): # , stopwordPath: str = None, delimWordPath: str = None):
        # If both Found and Initialized
        self.initialized = False
        self.stopWordList = list()
        self.delimWordList = list()

    def initializeFromPath(self, stopwordPath: str = "", delimWordPath: str = ""):
        if not os.path.exists(stopwordPath):
            print("Stop Word Path invalid")
            return

        if not os.path.exists(delimWordPath):
            print("Delim Word Path Invalid")
            return

        swLibList = [line.rstrip('\n') for line in open(stopwordPath,'r')]
        conjLibList = [line.rstrip('\n') for line in open("data/stoplist/中文分隔词词库.txt",'r')]
        self.initializeFromList(swLibList, conjLibList)
        return
        
    def initializeFromList(self, swList : List = None, dwList : List = None):
        self.stopWordList = swList
        self.delimWordList = dwList
        
        if len(self.stopWordList) == 0 or len(self.delimWordList) == 0:
            print("Empty Stop word list or deliminator word list, uninitialized")
            return
        else:
            self.initialized = True

    def extractKeywordFromPath(self, text : str, num_kw : int = 10):
        if not self.initialized:
            print("Not initialized")
            return 

        with open(text,'r') as fp:
            text = fp.read()
        return self.extractKeywordFromString(text, num_kw = num_kw)
        
    def extractKeywordFromString(self, text : str, num_kw : int = 10):
        rawtextList = pseg.cut(text)

        # Construct List of Phrases and Preliminary textList
        textList = []
        listofSingleWord = dict()
        lastWord = ''
        poSPrty = ['m','x','uj','ul','mq','u','v','f']
        meaningfulCount = 0
        checklist = []
        for eachWord, flag in rawtextList:
            checklist.append([eachWord,flag])
            if eachWord in self.delimWordList or not notNumStr(eachWord) or eachWord in self.stopWordList or flag in poSPrty or eachWord == '\n':
                if lastWord != '|':
                    textList.append("|")
                    lastWord = "|"
            elif eachWord not in self.stopWordList and eachWord != '\n':
                textList.append(eachWord)
                meaningfulCount += 1
                if eachWord not in listofSingleWord:
                    listofSingleWord[eachWord] = Word(eachWord)
                lastWord = ''

        # Construct List of list that has phrases as wrds
        newList = []
        tempList = []
        for everyWord in textList:
            if everyWord != '|':
                tempList.append(everyWord)
            else:
                newList.append(tempList)
                tempList = []

        tempStr = ''
        for everyWord in textList:
            if everyWord != '|':
                tempStr += everyWord + '|'
            else:
                if tempStr[:-1] not in listofSingleWord:
                    listofSingleWord[tempStr[:-1]] = Word(tempStr[:-1])
                    tempStr = ''

        # Update the entire List
        for everyPhrase in newList:
            res = ''
            for everyWord in everyPhrase:
                listofSingleWord[everyWord].updateOccur(len(everyPhrase))
                res += everyWord + '|'
            phraseKey = res[:-1]
            if phraseKey not in listofSingleWord:
                listofSingleWord[phraseKey] = Word(phraseKey)
            else:
                listofSingleWord[phraseKey].updateFreq()

        # Get score for entire Set
        outputList = dict()
        for everyPhrase in newList:

            if len(everyPhrase) > 5:
                continue
            score = 0
            phraseString = ''
            outStr = ''
            for everyWord in everyPhrase:
                score += listofSingleWord[everyWord].returnScore()
                phraseString += everyWord + '|'
                outStr += everyWord
            phraseKey = phraseString[:-1]
            freq = listofSingleWord[phraseKey].getFreq()
            if freq / meaningfulCount < 0.01 and freq < 3 :
                continue
            outputList[outStr] = score

        sorted_list = sorted(outputList.items(), key = operator.itemgetter(1), reverse = True)
        return sorted_list[:num_kw]


        