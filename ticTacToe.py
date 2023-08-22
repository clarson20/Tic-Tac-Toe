import os
import random
import time

# Essential Functions
def clear():
    os.system('clear')

def X_or_O():
    while True:
        letter = input(("Would you like to play as 'X' or 'O'?(X goes first)"))
        if letter == "X" or letter == "x":
            userLetter = "X"
            CPULetter = "O"
            return userLetter,CPULetter
        elif letter == "O" or letter == 'o':
            userLetter = "O"
            CPULetter = "X"
            return userLetter,CPULetter
        else:
            print("Please enter either 'X' or 'O'")
    
def displayBoard(boardValues):
    print("|---|---|---|")
    print("|-",boardValues[0][0],"-|-",boardValues[0][1],"-|-",boardValues[0][2],"-|", sep="")
    print("|---|---|---|")
    print("|-",boardValues[1][0],"-|-",boardValues[1][1],"-|-",boardValues[1][2],"-|", sep="")
    print("|---|---|---|")
    print("|-",boardValues[2][0],"-|-",boardValues[2][1],"-|-",boardValues[2][2],"-|", sep="")
    print("|---|---|---|")

def isOpen(boardValues,userInput):
    for row_index, row in enumerate(boardValues):
        for col_index, value in enumerate(row):
            if int(userInput) == value:
                return (row_index,col_index)
    return None

def placeMarker(boardValues, boardLocation, userLetter): #requires tuple as boardLocation
    boardValues[boardLocation[0]][boardLocation[1]] = userLetter

#User and CPU checking functions
def vertCheck(boardValues,XY,whichCol):
    counter = 0
    for row in boardValues:
        if row[whichCol] == XY:
            counter += 1
    return counter

def rowCheck(boardValues, XY,whichRow):
    counter = 0
    row = boardValues[whichRow]
    for col in row:
         if col == XY:
            counter += 1
    return counter

def crossCheck (boardValues, XY, left_or_right):
    counter = 0
    if left_or_right == "left" or left_or_right == "Left":
        for i in range(0,3):
            if boardValues[i][i] == XY:
                counter += 1
        return counter
    elif left_or_right == "right" or left_or_right == "Right":
        reverse_iterator = 2
        for i in range (0,3):
            if boardValues[i][reverse_iterator] == XY:
              counter += 1
            reverse_iterator -= 1
        return counter

def tieCheck(boardValues): #checks for tie by counting number of X and O characters on the board
    counter = 0
    for row in boardValues:
        for col in row:
            if col == "X" or col == "O":
               counter += 1
    return counter

def isGameOver(boardValues,XY):
    for i in range(0,3):
        if rowCheck(boardValues, XY, i) == 3:
            return True
    for i in range(0,3):
        if vertCheck(boardValues, XY, i) == 3:
            return True
    if crossCheck(boardValues, XY, "left") == 3:
        return True
    if crossCheck(boardValues, XY, "right") == 3:
        return True
    if tieCheck(boardValues) == 9:
        return "You tied..."
    return False
    
#CPU Checking Functions (only used for hard mode)
def vertCheckCPU(boardValues, whichCol): 
    for row_index, row in enumerate(boardValues):
        if row[whichCol] != "X" and row[whichCol] != "O":
            return (row_index, whichCol)
    return None

def rowCheckCPU(boardValues,whichRow): 
    row = boardValues[whichRow]
    for col_index, col in enumerate(row):
        if col != "X" and col != "O":
            return (whichRow, col_index)
    return None

def crossCheckCPU(boardValues, left_or_right):
    if left_or_right == "left" or left_or_right == "Left":
        for i in range(0,3):
            if boardValues[i][i] != "X" and boardValues[i][i] != "O":
                return (i,i)
    elif left_or_right == "right" or left_or_right == "Right":
        reverse_iterator = 2
        for i in range (0,3):
            if boardValues[i][reverse_iterator] != "X" and boardValues[i][reverse_iterator] != "O":
              return (i, reverse_iterator)
            reverse_iterator -= 1
    return None
    
#CPU Move Functions

def easyCPUmove (boardValues, CPULetter): #places marker at complete random
    openSpaceFound = False
    while openSpaceFound == False:
        
        cpuInput = isOpen(boardValues, random.randint(1,9))
        if cpuInput is not None:
            openSpaceFound = True
            placeMarker(boardValues, cpuInput, CPULetter)
    
def hardCPUOffense(boardValues, CPULetter): #checks for open spaces that would secure a CPU win

    for i in range(0,3): #checks for rows
        if rowCheck(boardValues, CPULetter, i) == 2:
            winningSpace = rowCheckCPU(boardValues, i)
            if winningSpace is not None:
                placeMarker(boardValues, winningSpace, CPULetter)
                return True
    for i in range (0,3): #checks for columns
        if vertCheck(boardValues, CPULetter, i) == 2:
            winningSpace = vertCheckCPU(boardValues, i)
            if winningSpace is not None:
                placeMarker(boardValues, winningSpace, CPULetter)
                return True
    if crossCheck(boardValues, CPULetter, "left") == 2: # top left to bottom right cross
        winningSpace = crossCheckCPU(boardValues, "left")
        if winningSpace is not None:
            placeMarker(boardValues, winningSpace, CPULetter)
            return True
    if crossCheck(boardValues, CPULetter, "right") == 2: # top right to bottom left cross
        if winningSpace is not None:
            placeMarker(boardValues, winningSpace, CPULetter)
            return True
    return False
        
def hardCPUDefense(boardValues, userLetter, CPULetter): #checks for open spaces to stop a user win 
    for i in range(0,3): #checks for rows
        if rowCheck(boardValues, userLetter, i) == 2:
            winningSpace = rowCheckCPU(boardValues, i)
            if winningSpace is not None:
                placeMarker(boardValues, winningSpace, CPULetter)
                return True
    for i in range (0,3): #checks for columns
        if vertCheck(boardValues, userLetter, i) == 2:
            winningSpace = vertCheckCPU(boardValues, i)
            if winningSpace is not None:
                placeMarker(boardValues, winningSpace, CPULetter)
                return True
    if crossCheck(boardValues, userLetter, "left") == 2: # top left to bottom right cross
        winningSpace = crossCheckCPU(boardValues, "left")
        if winningSpace is not None:
            placeMarker(boardValues, winningSpace, CPULetter)
            return True
    if crossCheck(boardValues, userLetter, "right") == 2: # top right to bottom left cross
        winningSpace = crossCheckCPU(boardValues, "right")
        if winningSpace is not None:
            placeMarker(boardValues, winningSpace, CPULetter)
            return True
    return False

def hardCPUMove(boardValues,userLetter,CPULetter): #first looks for the win, then looks to stop a user win
    if hardCPUOffense(boardValues, CPULetter) == False:
        if hardCPUDefense(boardValues, userLetter, CPULetter) == False:
            easyCPUmove(boardValues, CPULetter)

def mediumCPUMove(boardValues, userLetter, CPULetter): #executes the hard difficulty 50% of the time
    if random.randint(0,1) == 0:
        hardCPUMove(boardValues,userLetter,CPULetter)
    else:
        easyCPUmove(boardValues, CPULetter)

def cpuMove (boardValues,CPULetter, userLetter,difficulty):
    print("Computer's Turn:")
    if difficulty == "Easy":
        easyCPUmove(boardValues,CPULetter)
    elif difficulty == "Medium":
        mediumCPUMove(boardValues, userLetter,CPULetter)
    else:
        hardCPUMove(boardValues, userLetter, CPULetter)


        

boardValues = [

    [1,2,3],
    [4,5,6],
    [7,8,9],
]

badInput = True
GameOver = False
turnCounter = 0

#Selecting Letter and Difficulty
userLetter, CPULetter = X_or_O()
difficulty = input('Please choose between "Easy" "Medium" or "Hard". If you choose something else it will automatically be hard')
print(difficulty)

#Main
while GameOver == False:
    if turnCounter == 0 and userLetter == "O":
        cpuMove (boardValues, CPULetter, userLetter, difficulty)
        displayBoard(boardValues)
        time.sleep(2.5)
        clear()
    badInput = True
    displayBoard(boardValues)
    while badInput == True:
        userInput = input("Please select the space you would like to mark: ")
        openSpace = isOpen(boardValues, userInput)
        if openSpace is not None:
            badInput = False
            placeMarker(boardValues, openSpace, userLetter)
            clear()
            displayBoard(boardValues)
        else:
            print("Sorry, this space is taken. Please choose an open space")
    if isGameOver(boardValues, userLetter) == True:
        clear()
        print ("You won!!!")
        displayBoard(boardValues)
        break
    if isGameOver(boardValues, userLetter) == "You tied...":
        clear()
        displayBoard(boardValues)
        print ("You tied...")
        break
    cpuMove(boardValues, CPULetter, userLetter, difficulty)
    time.sleep(2.5)
    if isGameOver(boardValues, CPULetter) == True:
        clear()
        print ("You lost!!!")
        displayBoard(boardValues)
        break
    turnCounter += 1
    clear()
    