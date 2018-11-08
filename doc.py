#comapre length of original word to the lemma, see how much stuff it's scraping off
#check out skopt for optimizing
import re
import os
import pandas as pd

class Doc:
    def __init__(self,path,fileName):
            myFile = os.path.join(path, fileName)
            f = open(myFile, "r", encoding="utf8")
            text = f.read()
            f.close()
            myFile = os.path.join(path+"\\frequency_list", fileName)
            f = open(myFile, "r", encoding="utf8")
            lemmaText = f.read()
            f.close()
            self.name = fileName
            self.body = self.getTagFromOriginal(text, 'BODY')
            self.difficulty = int(self.getTagFromOriginal(text, 'DIFFICULTY').replace('+',''))
            self.lemmaList = {}
            self.missingList = {}
            self.readLemmaList(lemmaText)
            self.wordCount = self.wordCounter(self.body)
            self.wordLength = len(self.body)/self.wordCount
            self.sentenceCount = self.sentenceCounter(self.body)
            self.sentenceLength = self.wordCount / self.sentenceCount
            self.count = {}
            self.count['noun']=0
            self.count['verb']=0
            self.count['prep']=0
            self.count['part']=0
            self.count['conj']=0
            self.count['adv']=0
            self.count['adj']=0
            self.frequencyTable = pd.DataFrame(columns=['lemma','pos','freq'])
            self.p95 = 0 #95th percentile, based on the idea of i+1 might need to recalc since this may be an average while we want a the actual number
            self.lemmaCount = 0
            self.median = 0
            self.mode = 0
            self.mean = 0

    def getDataString(self):
        string = str(self.wordCount)+','+str(self.sentenceCount)+','+str(self.sentenceLength)+','+str(self.lemmaRatio)+','+str(self.p95)+','+str(self.mean)+','+str(self.median)+','+str(self.wordLength)
        for pos in self.count:
            string += (','+str(self.count[pos]))
        string += ','+str(self.difficulty)
        return string

    def getTagFromOriginal(self, text, tagName):
        tagStart = "<" + tagName + ">"
        tagEnd = "</" + tagName + ">"
        posStart = text.find(tagStart)
        if posStart != -1:
            posStart += len(tagStart)
            posEnd = text.find(tagEnd)
            tagContent = text[posStart:posEnd]
            return tagContent
        else:
            return ""

    def readLemmaList(self,text):
        dataList = text.split('\n')
        for line in dataList:
            if line != '':
                if line in self.lemmaList:
                    self.lemmaList[line] += 1
                else:
                    self.lemmaList[line] = 1

    def wordCounter(self, body):
        # Find all non-whitespace patterns.
        wordList = re.findall("(\S+)", body)
        [x for x in wordList if x]
        #wordList = list(filter(None,wordList))
        # Return length of resulting list.
        return len(wordList)

    def sentenceCounter(self, body):
        # Find all sentence endings.
        senList = re.findall("[.!?\n]+", body)
        [x for x in senList if x]
        #senList = list(filter(None,senList))
        # Return length of resulting list.
        return len(senList)

    def getKeyFromLemmaListLine(self, line):
        d = {}
        d = line.split(":::")
        pos = d[3]
        lemma = standardizeWord(d[1])
        key = ''
        if pos == 'conj_sub':
            pos = 'conj'
        if pos == 'part_verb':
            pos = 'part'
        if lemma == 'هل' and pos == 'part_interrog':
            pos = 'prep'
        if lemma == 'منذ' and pos == 'conj':
            pos = 'prep'
        if lemma == 'عند' and pos == 'noun':
            pos = 'prep'
        if pos != 'digit' and pos != 'noun_prop':
            key = lemma+":::"+pos
        return key

    def getFrequencyInfo(self):
        df = self.frequencyTable.groupby('pos').count()
        self.lemmaCount = df.lemma.sum()
        for i in self.count:
            if i in df.index:
                self.count[i]=df.loc[i,'lemma']/self.lemmaCount
        self.p95 = self.frequencyTable.freq.iloc[(round(len(self.frequencyTable.freq.index)*.05))]
        self.median = self.frequencyTable.freq.median()
        self.mean = self.frequencyTable.freq.mean()
        sum = self.frequencyTable.freq.sum()
        self.lemmaRatio = sum / len(self.lemmaList)

def standardizeWord(word):
    newWord = ''
    for i in range(0,len(word)):
        char = word[i]
        newWord += standardizeChar(char)
    return newWord

def standardizeChar(char):
    s = {}
    s['أ']='ا'
    s['ٱ']='ا'
    s['آ']='ا'
    s['ؤ']='و'
    if char in s:
        return s[char]
    else:
        return char