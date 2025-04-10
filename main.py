from guizero import App, Text, TextBox, PushButton,Window,Box,info
from word import Word
from wordList import WordList
import random
from cwmaker import makecrossword, updatecolour


app = App(visible=False)
welcome = Window(app,title = "crossword",visible=True)


def backtomain():
  
  inputown.hide()
  randomwords.hide()
  welcome.show()

def gotoinput():
  
  welcome.hide()
  inputown.show()

def initialisewordlist(list,num,topic,defs):
    global wordlistobj
    wordlistobj = WordList(list,num,topic,defs)
    getwordsinalist()

def gotocwboardrandom():
  if howmany.value != "" and topic.value != "":    
      try:
        num = int(howmany.value)
        randomwords.hide()
        cwwindow.show()
        initialisewordlist([],num,topic.value,None)
        for _ in range(2):
          updatecrosswordthing()
      except ValueError:
        randmessage.value = "please enter a number"
  else:
      randmessage.value = "please enter both values"


inputtedwordlist = []
inputteddefslist = []
def addword():
  global inputtedwordlist, inputteddefslist
  inputted = input_box.value
  tempdef = inpdefbox.value
  if inputted != "" and inputted not in inputtedwordlist and tempdef != "":
      input_box.value = ""
      inpdefbox.value = ""
      message.value = "added!"
      inputtedwordlist.append(inputted.upper())
      inputteddefslist.append(tempdef)
      words.value = inputtedwordlist


def deletelast():
  global inputtedwordlist
  if inputtedwordlist != []:
    inputtedwordlist.pop()
    words.value = inputtedwordlist
    message.value = "removed!"

def resetlist():
    global inputtedwordlist
    while len(inputtedwordlist) > 0:
        deletelast()
    message.value = "reset!"
    
def gotocwinputted():
    global inputtedwordlist,inputteddefslist
    inputown.hide()
    cwwindow.show()
    initialisewordlist(inputtedwordlist,None,None,inputteddefslist)
    for _ in range(2):
          updatecrosswordthing()
    
goinputwords = PushButton(welcome,text = "input your own words",command=gotoinput)
##inside inputown##
inputown = Window(app,visible = False)
backbutton = PushButton(inputown, command = backtomain, text = "go back")
message = Text(inputown,text = "Input your words!",color="Red")
wordtext = Text(inputown,text="word here")
input_box = TextBox(inputown)
deftext = Text(inputown,text = "definition here")
inpdefbox = TextBox(inputown)
addbutton = PushButton(inputown, text='add',command=addword)
deletebutton = PushButton(inputown, text='delete last',command=deletelast)
resetbutton = PushButton(inputown, text='reset',command=resetlist)
yw = Text(inputown,text = "your words:")
words = Text(inputown,text = "")
done = PushButton(inputown, text = "done",command = gotocwinputted)

##inside inputown##

def cwrandom():
  welcome.hide()
  randomwords.show()

gorandomwords = PushButton(welcome,text = "use random words",command=cwrandom)
##inside randomwords##
randomwords = Window(app,title = "Using Random Words",visible=False)
backbutton = PushButton(randomwords, command = backtomain, text = "go back")
randmessage = Text(randomwords, text ="",color="red")
topicText = Text(randomwords,text = "What topic do you want")
topic = TextBox(randomwords)
howmanytext = Text(randomwords,text = "how many words do you want")
howmany = TextBox(randomwords)
continuetocrossword = PushButton(randomwords,text = "continue",command = gotocwboardrandom)
##inside randomwords##

##AFTER THIS IS THE CROSSWORD##
cwwindow = Window(app,visible = False,title = "crossword",layout = "grid")
cwwindow.fullscreen = True

def getwordsinalist():#makes the variable wordsinalist to use for crossword and indexing
    global wordsinalist,toanswer
    wordsinalist = []
    for wordobj in wordlistobj.words:
        wordsinalist.append(wordobj.word)
    toanswer = wordsinalist[:]
    print(toanswer)
    setindexes()
    getplacements(wordsinalist)
    
    
def getplacements(wordsinalist):
    global placements, colourgrid
    placements = makecrossword(wordsinalist)
    colourgrid = updatecolour()
    

def setindexes():
    index = 1
    for wordobj in wordlistobj.words:
        wordobj.index = index
        index += 1
    for wordobj in wordlistobj.words:
        print(wordobj.index)
    
def updatecrosswordthing():
    for row in range(len(colourgrid)):
        for column in range(len(colourgrid[row])):
            if colourgrid[row][column] == "W":
                cwgrid[row][column].bg = "White"
    #for putting the numbers on the words
    for placement in placements:
        for word in wordlistobj.words:
            if word.word == placement:
                word.setparams(placements[placement][0],placements[placement][1],placements[placement][2])
    for word in wordlistobj.words:
        if word.orientation == "a":
            indexcoord = (int(word.y),int(word.x-1))
        else:
            indexcoord = (int(word.y-1),int(word.x))
        cwgrid[indexcoord[0]][indexcoord[1]].value = word.index
        cwgrid[indexcoord[0]][indexcoord[1]].bg = "orange"
    initialisedefinitions()


defbuttons = []


def initialisedefinitions():
    global defbuttons
    for i in range(len(wordlistobj.words)):
        defbuttons.append(None)
    defcount = 0
    for word in wordlistobj.words:
        defbuttons.append(PushButton(buttonbox, text = word.index,command=displaydef, args=[word.index], grid = [int(defcount),0],pady=1))
        defcount += 1

def displaydef(index):
    for word in wordlistobj.words:
        if word.index == index:
            therightword = word
            break
    deftext.value = therightword.definition

cwbox = Box(cwwindow,layout="grid",grid=[0,0],border = True)
gamebox = Box(cwwindow,layout="grid",grid=[1,0])

buttonbox = Box(gamebox, layout = "grid",grid=[0,0])

Width = 30
Height = 30
cwgrid = [[0 for i in range(Height)] for j in range(Width)]
#cwbox = Box(cwgrid,layout="grid",grid=[0,0],width=Width,height=Height,border=True)

for y in range(Width):
  for x in range(Height):
    cwgrid[y][x] = Text(cwbox,grid=[x+10,y+10],width=1  ,height=1,bg="light gray")

def takeawayfromlist(word):
    global toanswer
    toanswer.remove(word)
    print(toanswer)
    if len(toanswer) == 0:
        cwwindow.info("WELL DONE", "YOU WON!")
    

def correctanswer(word):    
    for wordobj in wordlistobj.words:
        if wordobj.word == word:
            theobj = wordobj
            break
    if theobj.orientation == "a":
        for i in range(len(theobj.word)):
            cwgrid[int(theobj.y)][int(theobj.x+i)].value = theobj.word[i]
    elif theobj.orientation == "d":
        for i in range(len(theobj.word)):
            cwgrid[int(theobj.y+i)][int(theobj.x)].value = theobj.word[i]
    
    takeawayfromlist(word)
    
def checkanswer():
    global toanswer
    if answerbox.value.upper() in toanswer:
        correctanswer(answerbox.value.upper())
    answerbox.value = ""

deftext = Text(gamebox, text = "",grid=[0,1],align="left")
answerbox = TextBox(gamebox,grid=[0,2])
submitanswer = PushButton(gamebox,grid=[0,3],command=checkanswer,text="submit")
