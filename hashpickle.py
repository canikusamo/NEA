import pickle


class Hashtable:

    def __init__(self):
        self.size = 1009#a large prime
        pickle_off = open("hashlist.pickle", 'rb')
        self.hashlist = pickle.load(pickle_off)

    def addworddef(self,word,defi):#hash word and store the tuple (word,defi) in the hashed place
        total = 0
        for letter in word:
            total += ord(letter)
        key = total % self.size
        placed = False
        while not placed:
            if self.hashlist[key] == None:
                self.hashlist[key] = (word,defi)
                placed = True
            else:
                key += 1
        
        
        
    
    def returndef(self,word): #return a definition given a word / return None if not in
        total = 0
        for letter in word:
            total += ord(letter)
        key = total % self.size
        while True:#we can use while true here because when something is returned it will break
            if self.hashlist[key] == None:
                return None
            elif self.hashlist[key][0] == word:
                return self.hashlist[key][1]
            else:#this means there was a colission
                key += 1
                
            
        
    def returnwholehash(self):
        return self.hashlist

    def picklehashlist(self):
        pickling_on = open("hashlist.pickle","wb")
        pickle.dump(self.hashlist, pickling_on)
        pickling_on.close()

        
    def resetpickle(self):#pickles an empty dictionary
        mpty = {}
        for i in range(self.size):
            mpty[i] = None
        pickling_on = open("hashlist.pickle","wb")
        pickle.dump(mpty, pickling_on)
        pickling_on.close()
    
    
