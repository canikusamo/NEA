from word import Word 
from hashpickle import Hashtable
import requests
import random
import re

class WordList:

    def __init__(self,wordsToAdd,numOfWords,topic,defs):
        hasht = Hashtable()
        self.words = []#holds the word objects
       
        self.defstoadd = defs
        self.wordsToAdd = wordsToAdd
 
        self.numOfWords = numOfWords
        self.topic = topic
        if wordsToAdd == []:#auto generate if no words given
            self._generatewords(hasht)
            hasht.picklehashlist()
        else:
            for (word,definition) in zip(self.wordsToAdd,self.defstoadd):
                self._addWord(word,definition)#add hasht insead of definition to revert to auto def
            #hasht.picklehashlist()
            random.shuffle(self.words)
            self.numOfWords = len(self.words)
            

    def _addWord(self,word,definition):
        #definition = self._getdef(word,hasht)
        self.words.append(Word(word,definition))
        
    def _getdef(self,word,hasht):#Now with hashtable in it!!
        
        hashdef = hasht.returndef(word)
        if hashdef == None:
          url = "https://wordsapiv1.p.rapidapi.com/words/"+word+"/definitions"
          headers = {"X-RapidAPI-Key": "89ed6ec070msha33388028a32ccbp11b72bjsnc882288cb5d3","X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"}
          checkifmeaning = requests.request("GET", url, headers=headers).json()
          try:
            checkifmeaning = checkifmeaning["message"]
            print(word," has no definition")
            return None
          except KeyError:
            try:
                definition = checkifmeaning["definitions"][0]["definition"]
            except IndexError:
                definition = "No."
                print("no definition could be found for",word)
            definition = checkifmeaning["definitions"][0]["definition"]
            isitin = self._findWholeWord(word)(definition)
            while isitin != None: 
              start, end = isitin.span()[0],isitin.span()[1] #span returns a tuple with the start and end index 
              definitionlists = [i for i in definition] 
              for x in range(start,end):
                definitionlists[x] = "_"
              definition = ""
              for j in definitionlists:
                definition += j
              isitin = self._findWholeWord(word)(definition) 
            #new 
            hasht.addworddef(word,definition)
            return definition
        else:
            return hashdef
            
            

    def _findWholeWord(self,w): #i copied this from stackoverflow it uses regular expresstions and finds the word match it returns 'None' if there is no match.
      return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


    def _generatewords(self,hasht):#generate random words
    #creates a word and definition
      response = requests.request("GET", "https://api.datamuse.com/words?ml="+self.topic).json()
      #print(response)  
      
      for _ in range(self.numOfWords):
        while True:
          wordtocheck = random.choice(response)["word"]
          if wordtocheck.upper() not in self.words and " " not in wordtocheck:#self explanatory
            hashdef = hasht.returndef(wordtocheck)
            if hashdef != None:
                definition = hashdef
                break
            url = "https://wordsapiv1.p.rapidapi.com/words/"+wordtocheck+"/definitions"
            headers = {"X-RapidAPI-Key": "89ed6ec070msha33388028a32ccbp11b72bjsnc882288cb5d3","X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"}
            checkifmeaning = requests.request("GET", url, headers=headers).json()
            try:
              checkifmeaning = checkifmeaning["message"]#message will only return something if there is no definition so if there is a definition it will return a type error
            except KeyError:
              try:
                definition = checkifmeaning["definitions"][0]["definition"]
                hasht.addworddef(wordtocheck,definition)
                break#break out of the finding word loop bcause its been found
              except IndexError:
                  pass#this will make sure empty definitions wont be picked
        
        isitin = self._findWholeWord(wordtocheck)(definition)
        while isitin != None: 
          start, end = isitin.span()[0],isitin.span()[1] #span returns a tuple with the start and end index 
          definitionlists = [i for i in definition] 
          for x in range(start,end):
            definitionlists[x] = "_"
          definition = ""
          for j in definitionlists:
            definition += j
          isitin = self._findWholeWord(wordtocheck)(definition)  
        

        #create object of word
        self.words.append(Word(wordtocheck.upper(),str(definition+" ("+str(len(wordtocheck))+" letters)")))




