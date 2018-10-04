import re
class LangDoc:
	''' this is a descriptor '''
	''' things that are the same for all instances'''
	language = 'french'
	
	def __init__(self, originalText, lemmaText, title, difficulty = -1):
		'''things that are different for each class'''
		self.originalText = originalText
		self.lemmaText = lemmaText
		self.title = title
		self.difficulty = difficulty
		self.body = ""
		self.wordCount = 0
		self.sentenceCount = 1
		self.wordsPerSentence = 0
		self.lemmaList = {}
		self.CalcData()
	
	def GetTagFromOriginal(self, tagName):
		tagStart = "<" + tagName + ">"
		tagEnd = "</" + tagName + ">"
		text = self.originalText
		posStart = text.find(tagStart)
		if posStart != -1:
			posStart += len(tagStart)
			posEnd = text.find(tagEnd)
			tagContent = text[posStart:posEnd]
			return tagContent
		else:
			return ""
	
	def WordCounter(self, body):
		# Find all non-whitespace patterns.
		wordList = re.findall("(\S+)", body)
		[x for x in wordList if x]
		#wordList = list(filter(None,wordList))
		# Return length of resulting list.
		return len(wordList)
		
	def SentenceCounter(self, body):
		# Find all sentence endings.
		senList = re.findall("[.!?\n]+", body)
		[x for x in senList if x]
		#senList = list(filter(None,senList))
		# Return length of resulting list.
		return len(senList)
	
	def GetLemmaList(self):
		lemmas = self.lemmaText.split("\n")
		for lemma in lemmas:
			#check first char if Arabic
			if len(lemma) > 0:
				if self.IsArabic(lemma[0]):
					if lemma in self.lemmaList:
						self.lemmaList[lemma] += 1
					else:
						self.lemmaList[lemma] = 1
	
	def CalcData(self):
		self.body = self.GetTagFromOriginal("BODY")
		self.difficulty = self.GetTagFromOriginal("DIFFICULTY")
		self.wordCount = self.WordCounter(self.body)
		self.sentenceCount = self.SentenceCounter(self.body)
		if self.sentenceCount > 0:
			self.wordsPerSentence = self.wordCount / self.sentenceCount
		self.GetLemmaList()
			
	def IsArabic(self, char):
		charIndex = ord(char)
		#check if char code is within the Arabic font range
		check = (charIndex >= 1536 and charIndex <= 1791)
		return check
		
	def GetDataString(self):
		dataString = str(self.wordCount) + "," + str(self.sentenceCount) + "," + str(self.wordsPerSentence) + "," + str(len(self.lemmaList)) + "," + str(self.difficulty)
		return dataString