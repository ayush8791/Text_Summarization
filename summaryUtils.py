#region Imports
import numpy as np
import pandas as pd
import nltk
import re
import heapq
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')

#endregion

def cleanText(text):
  ''' Takes Text(String) returns Sanitised Text
    Removes special characters and extra spaces '''

  text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  return text

def extractSentences(text):
  '''Extract Sentences from text using '.' '''

  return sent_tokenize(text)


def getWeightedFrequencies(frequencies): 
  ''' Takes Word Frequencies 
    Returns Weighted Frequency '''

  maxFrequency = max(frequencies.values())

  for word in frequencies.keys():
    frequencies[word] = frequencies[word] / maxFrequency
  return frequencies

def getWordFrequency(text):
  ''' Returns Word Frequency
    Filters StopWords '''

  stopwords = nltk.corpus.stopwords.words('english')
  text = text.lower()
  wordFrequencies = {}

  for word in nltk.word_tokenize(text):
    if word not in stopwords:
      if word not in wordFrequencies.keys():
        wordFrequencies[word] = 1
      else:
        wordFrequencies[word]+=1
  return getWeightedFrequencies(wordFrequencies)

def getSentScores(sentences, weightedWordFreq):
  ''' Returns Sentence Scores based on Word
    Freq '''
  sentScore = {}
  stopwords = nltk.corpus.stopwords.words('english')
  sentCount = len(sentences)

  for num , sent in enumerate(sentences, start = 1):
    for word in nltk.word_tokenize(sent.lower()):
      if word not in stopwords:
        if word in weightedWordFreq.keys():
          if len(sent.split(' ')) < 30:
            if sent not in sentScore.keys():
              sentScore[sent] = weightedWordFreq[word]
            else:
              sentScore[sent] += weightedWordFreq[word]
    if sent in sentScore.keys():
      sentScore[sent] += (sentCount - num) / sentCount
  print("Max Sentence Score is : ")
  print(max(sentScore.values()))
  print(len(sentences))
  return sentScore

def getSummary(originalText):
  ''' Returns Text Summary '''
  formattedText = cleanText(originalText)
  sentences = extractSentences(originalText)
  wordFreq = getWordFrequency(formattedText)
  sentScores = getSentScores(sentences , wordFreq)

  topSent = heapq.nlargest(7, sentScores, key =  sentScores.get )

  return ''.join(topSent)

