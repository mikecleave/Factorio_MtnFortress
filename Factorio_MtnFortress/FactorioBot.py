import pyautogui as pya
import pydirectinput #https://github.com/learncodebygaming/pydirectinput
import time
import keyboard
import sys
from sendKeys import *
from threading import Thread

pya.FAILSAFE = True #When fail-safe mode is True, moving the mouse to the upper-left will raise a pyautogui.FailSafeException that can abort your program


#Need to use the WASD letters.
firstDir = "w"
secondDir = "d"

firstDirTime = 5
secondDirTime = 2

activeMiningTime = 0
noRocksTimer = 0
noRocksTimerKillTime = 5

noRocksTimerStarted = False
print(noRocksTimerStarted)
print(type(noRocksTimerStarted))

print("TEST")

keys = {
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "a": 0x41,
    "c": 0x43,
    "d": 0x44,
    "q": 0x51,
    "s": 0x53,    
    "w": 0x57,  
    "f9": 0x78,
    "space": 0x20
}

pya.size()
centerScreen = pya.size()
centerScreen = centerScreen.width/2, centerScreen.height/2 - 15


def main():
    SendKey(keys['f9']) #Press the F9 key to zoom the the preset amount.
    ShiftSendKey(keys['0']) # Shift + 0
    PressKey(keys['space'])

    while keyboard.is_pressed('i') == False: #If 'i' is pressed it will stop the program. 
        #Mine first direction
        mine(firstDir, firstDirTime)
        
        #Mine second direction
        mine(secondDir, secondDirTime)
        
        #Mine inverse of first direction
        mine(invertDir(firstDir), firstDirTime)
        
        #Mine second direction
        mine(secondDir, secondDirTime)
                        
    ReleaseKey(keys['space'])

def invertDir(Dir):
    if Dir == "a": #Left to right
        newDir = "d"

    elif Dir == "d": #Right to left
        newDir = "a"

    elif Dir == "w": #Up to down
        newDir = "s"

    elif Dir == "s": #Down to up
        newDir = "w"

    return newDir

def mine(direction, mineTime):
    global noRocksTimer
    global noRocksTimerStarted
    global noRocksTimerKillTime
    
    print('mining')
    checkForDeath()
    
    if direction == "w":
        xOffset = 0
        yOffset = -50
        
    elif direction == "a":
        xOffset = -20
        yOffset = 0
        
    elif direction == "s":
        xOffset = 0
        yOffset = 20

    elif direction == "d":
        xOffset = 20
        yOffset = 0
        
    pya.moveTo(centerScreen[0]+xOffset, centerScreen[1]+yOffset)    
    pya.mouseDown(button='right')  # press the right mouse button down

    start = time.time()
    while time.time() - start < mineTime:

        if noRocksTimer > noRocksTimerKillTime: #If I don't mine rocks for x seconds stop the program. 
            releaseAllKeys()
            sys.exit("Timer > x sec")
            
        print("Holding the " + direction + " key.")
        killSwitchCheck()
        checkForLowHealth()
        checkForSpaceship()
        checkForChest()
        checkForDeath()
        PressKey(keys[direction])

        checkForNoRocks()
                                        
    ReleaseKey(keys[direction])    
    pya.mouseUp(button='right')  # Releases the right mouse button

    noRocksTimer = 0
    noRocksTimerStarted = False
    
    checkForLowHealth()
    placeChest(direction) #Place a chest behind me
    depositOre()


def checkForNoRocks():
    global noRocksTimer
    global noRocksTimerStarted
    
    print("Checking for rocks to mine")
    if (pya.locateOnScreen('img/entityBackgroundColor.png', region = (1800,470,100,200), confidence=0.9) is None): #Checks if there are no rocks to mine. 
        print("No rocks found")

        if (noRocksTimerStarted == False):
            print("Start rock timer")
            Thread(target = noRocksTimerFunction).start()
    else:
        print("Rocks found! :)")
        noRocksTimerStarted = False
        noRocksTimer = 0


def noRocksTimerFunction():
    global noRocksTimer
    global noRocksTimerStarted
    global noRocksTimerKillTime
    print("Starting noRocksTimer")
    
    noRocksTimerStarted = True
    startTime = time.time()
    
    while noRocksTimerStarted == True:
        noRocksTimer = time.time() - startTime
        print("no rock timer: ", noRocksTimer)
        if noRocksTimer > noRocksTimerKillTime or keyboard.is_pressed('i') == True: #Check if I want to stop the program
            releaseAllKeys()
            sys.exit("Timer > x sec OR manually stopped")
        

    
def checkForLowHealth():
    if (pya.locateOnScreen('img/healthBar2.png', region = (600,894,600,20), confidence=0.9) is not None): #Checks if the cursor is over a spaceship that can not be mined.     
        print("Low Health")
        SendKey(keys['3']) # Select the fish
        pya.click() # Eat the fish

def checkForSpaceship():
    if (pya.locateOnScreen('img/spaceship.png', region = (1600,480,100,40), confidence=0.9) is not None): #Checks if the cursor is over a spaceship that can not be mined.
        print("Spaceship found")

        for x in keys:
            print("Releasing the " + x + " key")
            ReleaseKey(keys[x])
            
        HoldKey(keys['c'], 2) # The code does not continue until the time is up.
        PressKey(keys['space'])

def checkForChest(): #Checks for a chest that can't be picked up.
    if (pya.locateOnScreen('img/chest.png', region = (1600,480,100,40), confidence=0.9) is not None): #Checks if the cursor is over a chest that can not be mined.
        print("Chest found")

        for x in keys:
            print("Releasing the " + x + " key")
            ReleaseKey(keys[x])
            
        HoldKey(keys['c'], 2) # The code does not continue until the time is up.
        PressKey(keys['space'])

def killSwitchCheck():
    if keyboard.is_pressed('i') == True: #Check if I want to stop the program
        releaseAllKeys()        
        sys.exit("Program manually stopped")
        

def placeChest(direction):
    print('place chest')
    horizontalOffset = 0
    verticalOffset = 0

    if direction == "a":
        horizontalOffset = 30

    elif direction == "d":
        horizontalOffset = -30

    elif direction == "w":
        verticalOffset = 30

    elif direction == "s":
        verticalOffset = -30
    
    SendKey(keys['1'])
    pya.moveTo(centerScreen[0]+horizontalOffset, centerScreen[1]+verticalOffset)    
    pya.click()
    SendKey(keys['q'])
    
def depositEverything():
    print('deposit everything')
    pya.moveTo(pya.locateOnScreen('img/box.png'))
    pya.click()

def depositOre():
    print('deposit ore')
    pya.moveTo(pya.locateOnScreen('img/box.png'))
    pya.click(button='right')
    
def checkForDeath():
    print('check for death')
    if pya.locateOnScreen('img/dead.png') != None:
        releaseAllKeys()            
        sys.exit("You are dead")

def releaseAllKeys():
    print('Releasing all keys')
    pya.mouseUp(button='left')  # Releases the left mouse button
    pya.mouseUp(button='right')  # Releases the right mouse button
    for x in keys:
        print("Releasing the " + x + " key")
        ReleaseKey(keys[x])
    

time.sleep(3)
print("Start")

main()

print("Done")
