from langdoc import LangDoc
###PURPOSE to explore how classes work

		
doc1 = LangDoc('source.com', 'test')
print(doc1.wordCount, doc1.difficulty, doc1.source, doc1.language)
doc1.difficulty = 2
print(doc1.wordCount, doc1.difficulty, doc1.source, doc1.language)
doc1.changeDifficulty(3)

print("difficulty of %s is %d" % (doc1.title, doc1.difficulty))

doc2 = LangDoc('utah.edu', 'test', 2)

print("language of doc 1 is %s" %(doc1.language))
print("language of doc 2 is %s" %(doc2.language))

doc2.language = 'french'

print("language of doc 1 is %s" %(doc1.language))
print("language of doc 2 is %s" %(doc2.language))

LangDoc.language = 'spanish'
doc3 = LangDoc('byu.edu', 'test', 3)

print("language of doc 1 is %s" %(doc1.language))
print("language of doc 2 is %s" %(doc2.language))
print("language of doc 3 is %s" %(doc3.language))

