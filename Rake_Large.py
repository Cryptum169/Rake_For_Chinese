import jieba
import jieba.posseg as pseg
import operator
import json
from collections import Counter

# 增加尝试图库

class Word():
    def __init__(self, char, freq = 0, deg = 0):
        self.freq = freq
        self.deg = deg
        self.char = char

    def returnScore(self):
        return self.deg/self.freq

    def updateOccur(self, phraseLength):
        self.freq += 1
        self.deg += phraseLength

    def getChar(self):
        return self.char

    def updateFreq(self):
        self.freq += 1

    def getFreq(self):
        return self.freq

def notNumStr(instr):
    for item in instr:
        if '\u0041' <= item <= '\u005a' or ('\u0061' <= item <='\u007a') or item.isdigit():
            return False
    return True

def readSingleTestCases(testFile):
    with open(testFile) as json_data:
        try:
            testData = json.load(json_data)
        except:
            # This try block deals with incorrect json format that has ' instead of "
            data = json_data.read().replace("'",'"')
            try:
                testData = json.loads(data)
                # This try block deals with empty transcript file
            except:
                return ""
    returnString = ""
    for item in testData:
        try:
            returnString += item['text']
        except:
            returnString += item['statement']
    return returnString

# Construct Stopword Lib
swLibList = [line.rstrip('\n') for line in open("/data/stoplist/中文停用词表(1208个).txt",'r')]

# Construct Phrase Deliminator Lib
conjLibList = [line.rstrip('\n') for line in open("/data/stoplist/中文分隔词词库.txt",'r')]

# Obtain a list of individual words
fp = open("文本7.txt",'r')
rawText = fp.read().replace(' ', '').replace('\n', '。')
fp.close()
# rawText = readSingleTestCases("14_20180514_1600_channel_0.txt")
# rawtextList = jieba.cut(rawText)
rawtextList = pseg.cut(rawText)

# Construct List of Phrases and Preliminary textList
textList = []
listofSingleWord = dict()
lastWord = ''
stopPrty = ['m','x','uj','ul','mq','u','v','f'] # ['v', 'vi', 'vl']
meaningfulCount = 0
checklist = []
for eachWord, flag in rawtextList:
    checklist.append([eachWord,flag])
    if eachWord in conjLibList or not notNumStr(eachWord) or eachWord in swLibList or flag in stopPrty or eachWord == '\n':
        if lastWord != '|':
            textList.append("|")
            lastWord = "|"
    elif eachWord not in swLibList and eachWord != '\n':
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
print(sorted_list[:10])