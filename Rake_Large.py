import jieba
import jieba.posseg as pseg
import operator
import json

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
swLibList = [line.rstrip('\n') for line in open("中文停用词表(1208个).txt",'r')]

# Construct Phrase Deliminator Lib
conjLibList = [line.rstrip('\n') for line in open("中文分隔词词库.txt",'r')]

# Obtain a list of individual words
fp = open("文本1.txt",'r')
rawText = fp.read()
fp.close()
# rawText = readSingleTestCases("14_20180514_1600_channel_0.txt")
# rawtextList = jieba.cut(rawText)
rawtextList = pseg.cut(rawText)

# Construct List of Phrases and Preliminary textList
phraseList = [""]
textList = []
outputList = []
lastWord = ''
for eachWord, flag in rawtextList:
    if eachWord in conjLibList or not notNumStr(eachWord):
        if lastWord != '|':
            textList.append("|")
            lastWord = "|"
    elif eachWord not in swLibList and flag != 'v' and eachWord != '\n':
        textList.append(eachWord)
        outputList.append(eachWord)
        lastWord = ''

print(textList)

if False:
    # Construct Word to Score Matrix
    listOfWords = dict()
    for phrase in textList:
            for char in phrase:
                if char not in listOfWords:
                    listOfWords[char] = Word(char,1,len(phrase))
                else:
                    listOfWords[char].updateOccur(len(phrase))

    # Calculate Phrase Matrix
    outputList = dict()
    for phrase in textList:
        if len(phrase) > 1:
            score = 0
            for char in phrase:
                score += (listOfWords[char]).returnScore()
            outputList[phrase] = score / len(phrase)

    # Sort
    sorted_list = sorted(outputList.items(), key = operator.itemgetter(1), reverse = True)
    print(sorted_list[:10])