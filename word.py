#class for a word object

class Word:

    #constructor method
    def __init__(self,word,definition):
        self.word = word
        self.lenght = len(word)
        self.definition = definition
        self.placed = False
        self.index = 0
        self.orientation = None
        self.x = None
        self.y = None
        print(self.word,"Created")

    #getter to return the word 
    def getWord(self):
        return self.word

    def setparams(self,orientation,startx,starty):
        self.placed = True
        self.orientation = orientation
        self.y = starty
        self.x = startx

    
        