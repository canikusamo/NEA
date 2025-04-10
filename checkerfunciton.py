Height, Width = 40,40





def generatewordcoords(word,downacross,startx,starty):#returns a list of coord sthat the word will occupy (needed for the check)
    coordlist = []
    if downacross == "a":
        for i in range(len(word)):
            coordlist.append((int(startx+i),int(starty)))
    elif downacross == "d":
        for i in range(len(word)):
            coordlist.append((int(startx),int(starty+i)))
    else:
        print("Error: Invalid downacross for the generatecoords function (should be a or d)")
    return coordlist
    
def calculateaura(word,downacross,startx,starty):
    auracoords = []
    if downacross == "a":
        for i in range(len(word)+2):
            auracoords.append((int(startx+i-1),int(starty-1)))
            auracoords.append((int(startx+i-1),int(starty)))
            auracoords.append((int(startx+i-1),int(starty+1)))
            
    elif downacross == "d":
        for i in range(len(word)+2):
            auracoords.append((int(startx-1),int(starty+i-1)))
            auracoords.append((int(startx),int(starty+i-1)))
            auracoords.append((int(startx+1),int(starty+i-1)))
    else:
        print("Error: Invalid downacross for the generatecoords function (should be a or d)")
    return auracoords








def bbcf(wordtoplace,downacross,startx,starty,wordlen,wordtostick):#big brain check function
    global placements
    if startx < 0 or starty < 0 or startx > Width or starty > Height or startx+wordlen > Width or starty+wordlen > Height:#out of bounds check
      return False
    localplacements = placements
    localplacements.remove(wordtostick)#we dont want to check collisions with this because we want to stick to it
    auralist = []
    for placement in placements:#generate all the auras for previous placements
        auralist.append(calculateaura(placement,placements[placement][0],placements[placement][1],placements[placement][2]))
    auralist = list(dict.fromkeys(auralist))#removes duplicates
    wordcoords = generatewordcoords(wordtoplace,downacross,startx,starty)
    for i in wordcoords:
        if i in auralist:
            return False
    return True
    #this should be better than below but if issues change to bottom

    
    #for i in wordcoords:
        #if i in auralist:#this means it collides with another word's "aura"
            #return False
       # else: 
            #return True

    