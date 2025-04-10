import random
import checkerfunciton as check
global placements
global uhohqm

uhohqm = True# variable that is True if the crossword is not valid
placements = {}#a dictionary to reference back where a word was placed
Width = 30
Height = 30
class grid:
    def __init__(self,width,height,cw):
        self.width = width
        self.heigh = height
        self.cw = cw
        mygrid = []
        for i in range(height):
            row = []
            for j in range(width):
                if self.cw == "w":
                    row.append(" ")
                elif self.cw == "c":
                    row.append("G")
            mygrid.append(row)

        self.thegrid = mygrid
    
    def display(self):
        for i in self.thegrid:
            print(i)
    def returnthegrid(self):
      return(self.thegrid)

            
    def placeword(self,word,downacross,startx,starty):#places word on given coordinates, returns true if successful and false if not
        word  = word.upper()
        
        global placements
        placements[word] = [downacross,startx,starty]
        if self.cw == "w":
            if downacross == "a":
                try:
                    self.thegrid[int(starty)][int(startx+len(word)-1)] = word[int(len(word)-1)]#trying the most exptreme value to see if its out of range to stop the interaction before it happens
                    for i in range(len(word)-1):
                        self.thegrid[int(starty)][int(startx+i)] = word[i]
                    return True
                except IndexError:
                    return False
            if downacross == "d":
                try:
                    self.thegrid[int(starty+len(word)-1)][int(startx)] = word[int(len(word)-1)]#trying the most exptreme value to see if its out of range to stop the interaction before it happens
                    for i in range(len(word)-1):
                        self.thegrid[int(int(starty+i))][int(startx)] = word[i]
                    return True
                except IndexError:
                    return False
        elif self.cw == "c":
            if downacross == "a":
                try:
                    self.thegrid[starty][int(startx+len(word)-1)] = "W"#trying the most exptreme value to see if its out of range to stop the interaction before it happens
                    for i in range(len(word)-1):
                        self.thegrid[starty][startx+i] = "W"#w represents white colour
                    return True
                except IndexError:
                    return False
            if downacross == "d":
                try:
                    self.thegrid[int(starty+len(word)-1)][startx] = "W"#trying the most exptreme value to see if its out of range to stop the interaction before it happens
                    for i in range(len(word)-1):
                        self.thegrid[starty+i][startx] = "W"
                    return True
                except IndexError:
                    return False

def range_overlapping(x, y):
    if x.start == x.stop or y.start == y.stop:
        return False
    return x.start <= y.stop and y.start <= x.stop
#returns true if two ranges overlap


def flatten(array):
  flat = []
  for lst in array:
    for item in lst:
      flat.append(item)
  return flat

def bbcf(wordtoplace,downacross,startx,starty,wordlen,wordtostick):#big brain check function
    global placements
    if startx < 0 or starty < 0 or startx > Width or starty > Height or startx+wordlen > Width or starty+wordlen > Height:#out of bounds check
        return False
    localplacements = {}
    for item in placements:
        localplacements[item] = placements[item]
    
    localplacements.pop(wordtostick)#we dont want to check collisions with this because we want to stick to it
    auralist = []
    for placement in localplacements:#generate all the auras for previous placements
        auralist.append(check.calculateaura(placement,placements[placement][0],placements[placement][1],placements[placement][2]))
    auralist = flatten(auralist)
    wordcoords = check.generatewordcoords(wordtoplace,downacross,startx,starty)
    valid = True
    for i in wordcoords:
        if i in auralist:#this means it collides with another word's "aura"
            valid = False
        else: 
            pass
            
    return valid




def findcommonv2(word1,word2):#returns all combinations in format (indexword1,indexword2) and false if none
  resultlist = []
  for element in range(len(word1)):
    result = []
    offset = -1
    while True:
      try:
        offset = word2.index(word1[element], offset+1)
      except ValueError:
        if len(result) != 0:
          resultlist.append(result)
        break
      result.append((element,offset))
  resultlist = flatten(resultlist)
  random.shuffle(resultlist)#we shuffle so that every generated crossword is unique
  if len(resultlist) == 0:
    return False
  else:
    return resultlist

 
##GEN 1

def findcommon(word1,word2):
    for i in word1:
        if word2.find(i) != -1:
            return word2.find(i)
    return False

##GEN 1


def listtocrossword(oldwordlist):
    global uhohqm
    uhohqm = False
    global placements
    wordlist = []
    for i in oldwordlist:
      wordlist.append(i.upper())
    wordlist = list(sorted(wordlist,key=len))#orders words in size order
    wordtoplace = wordlist[-1]
    wordlist.remove(wordtoplace)#removes the biggest word and makes it the word to place
    wordgrid.placeword(wordtoplace,"a",(Width-len(wordtoplace))/2,Height/2)#place the first word in the middle and across
    mostrecent = list(placements)[len(placements)-1]#the most recent placement
    wordtoplace = wordlist[-1]
    while len(wordlist) > 0:
        mostrecent = random.choice(list(placements))#the word that that the other word will stick to
        wordtoplace = wordlist[-1]
        #print(wordtoplace,mostrecent)
        foundindex = findcommonv2(wordtoplace,mostrecent)
        count = 0
        count2 = 2
        while foundindex == False:#this tries to find any two compatible words
            count += 1
            if count > len(wordlist)-1 and count2 < len(placements)+1:
                count = 0
                mostrecent = list(placements)[len(placements)-count2]
                foundindex = findcommonv2(wordtoplace,mostrecent)
                count2 +=1
            elif count2 > len(placements):
              print("uncompatible")#hopefully this wont happen
            else:
                wordtoplace = wordlist[-1-count]
                foundindex = findcommonv2(wordtoplace,mostrecent)
            
        wordlist.remove(wordtoplace)
        previous = placements[mostrecent.upper()]
        if previous[0] == "a":#if its across
                #then we know the next will be down
                #x was changing now y will change
                offset = foundindex[0][0]#this will give the index of the common letter in the new word that will be placed
                startx = previous[1]+foundindex[0][1]
                starty = previous[2]-offset
                count3 = 1
                check = bbcf(wordtoplace,"d",startx,starty,len(wordtoplace),mostrecent.upper())
                while check == False:
                  if count3 > len(foundindex)-1:
                    #print("uh oh fixd")#hopefully this wont happen
                    uhohqm = True
                    break
                  else:
                    offset = foundindex[count3][0]
                    startx = previous[1]+foundindex[count3][1]
                    starty = previous[2]-offset
                    count3 += 1
                    check = bbcf(wordtoplace,"d",startx,starty,len(wordtoplace),mostrecent.upper())
                if count3 <= len(foundindex):
                  wordgrid.placeword(wordtoplace,"d",startx,starty)
                  #wordgrid.display()
                

        else:#if its down
                offset = foundindex[0][0]
                startx = previous[1]-offset
                starty = previous[2]+foundindex[0][1]
                count3 = 1
                check = bbcf(wordtoplace,"a",startx,starty,len(wordtoplace),mostrecent.upper())
                while check == False:
                  if count3 > len(foundindex)-1:
                    #print("uh oh")#hopefully this wont happen
                    uhohqm = True
                    break
                  else:
                    offset = foundindex[count3][0]
                    startx = previous[1]-offset
                    starty = previous[2]+foundindex[count3][1]
                    count3 += 1
                    check = bbcf(wordtoplace,"a",startx,starty,len(wordtoplace),mostrecent.upper())
                if count3 <= len(foundindex):
                  wordgrid.placeword(wordtoplace,"a",startx,starty)
                  #wordgrid.display()
    #wordgrid.display()

def updatecolour():
  mygrid = []
  for i in range(Height):
    row = []
    for j in range(Width):
      row.append(" ")
    mygrid.append(row)
  tocopy = wordgrid.returnthegrid()
  for row in range(len(tocopy)):
    for column in range(len(tocopy[row])):
      if tocopy[row][column] == " ":
        mygrid[row][column] = " "
      else:
        mygrid[row][column] = "W"
  return mygrid
    
def makecrossword(wordlist):
    global placements
    global wordgrid
    global uhohqm
    wordgrid = grid(Width,Height,"w")#initialise the two grids
    #wordlist = ["gamersunite","radicalisation","coconut","shutup","words","wire","fiddlesticks"]
    counterrrrr = 0
    while uhohqm == True:
        counterrrrr += 1
        if counterrrrr == 1000:
            print("incompatible")
            break
        print(counterrrrr)
        wordgrid = grid(Width,Height,"w")
        placements = {}
        listtocrossword(wordlist)
        #updatecolour()
    wordgrid.display()
    print(placements)
    return placements
    
    #the problem atm is either the check function is not working or the loop that goes with it because sometimes words overlap
    #also idded -1 to the low and +1 to the high of the ranges for the check function, those may not be the best idea maybe remove them
    