from tkinter import E
from numpy import e
import pyautogui as pya
import pydirectinput #https://github.com/learncodebygaming/pydirectinput
import time
import keyboard
import sys
from sendKeys import *
from threading import Thread

pya.FAILSAFE = True #When fail-safe mode is True, moving the mouse to the upper-left will raise a pyautogui.FailSafeException that can abort your program.

imageFilePath = "C:/Users/Mike/Documents/Factorio_MtnFortress/Factorio_MtnFortress/img/"

#Coordinates of a cube covering the personal logistics GUI. Ensures only icons are selected in it instead of your hotbar or inventory. 
x1 = 700
y1 = 200
x2 = 1215
y2 = 580

keys = { # msdn.microsoft.com/en-us/library/dd375731
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "a": 0x41,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "q": 0x51,
    "s": 0x53,    
    "w": 0x57,  
    "f9": 0x78,
    "space": 0x20,
}

requestedItems = {
    "woodChest": {'min': 0, 'max': 0, 'category': 'logistics', 'fileName': imageFilePath+'woodChest.png'},
    "ironChest": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'ironChest.png'},
    "steelChest": {'min': 50, 'max': 200, 'category': 'logistics', 'fileName': imageFilePath+'steelChest.png'},
    "storageTank": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'storageTank.png'},    
    
    "beltRed": {'min': 400, 'max': 400, 'category': 'logistics', 'fileName': imageFilePath+'beltRed.png'},
    "undergroundBeltRed": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'undergroundBeltRed.png'},
    "splitterRed": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'splitterRed.png'},

    "inserter": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'inserter.png'},
    "longInserter": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'longInserter.png'},
    "fastInserter": {'min': 50, 'max': 100, 'category': 'logistics', 'fileName': imageFilePath+'fastInserter.png'},
    "filterInserter": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'filterInserter.png'},
    "stackInserter": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'stackInserter.png'},
    
    "smallPole": {'min': 0, 'max': 0, 'category': 'logistics', 'fileName': imageFilePath+'smallPole.png'},
    "mediumPole": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'mediumPole.png'},
    "bigPole": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'bigPole.png'},
    "substation": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'substation.png'},

    "pipe": {'min': 100, 'max': 300, 'category': 'logistics', 'fileName': imageFilePath+'pipe.png'},
    "undergroundPipe": {'min': 50, 'max': 100, 'category': 'logistics', 'fileName': imageFilePath+'undergroundPipe.png'},
    "pump": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'pump.png'},

    "activeProviderChest": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'activeProviderChest.png'},
    "providerChest": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'providerChest.png'},
    "storageChest": {'min': 50, 'max': 200, 'category': 'logistics', 'fileName': imageFilePath+'storageChest.png'},
    "bufferChest": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'bufferChest.png'},
    "requesterChest": {'min': 50, 'max': 50, 'category': 'logistics', 'fileName': imageFilePath+'requesterChest.png'},
    "roboport": {'min': 10, 'max': 10, 'category': 'logistics', 'fileName': imageFilePath+'roboport.png'},
    

    "ironPlate": {'min': 400, 'max': 1000, 'category': 'products', 'fileName': imageFilePath+'ironPlate.png'},
    "copperPlate": {'min': 400, 'max': 1000, 'category': 'products', 'fileName': imageFilePath+'copperPlate.png'},
    "steel": {'min': 400, 'max': 1000, 'category': 'products', 'fileName': imageFilePath+'steel.png'},
    
    "greenCirc": {'min': 200, 'max': 400, 'category': 'products', 'fileName': imageFilePath+'greenCirc.png'},
    "redCirc": {'min': 200, 'max': 400, 'category': 'products', 'fileName': imageFilePath+'redCirc.png'},
    "blueCirc": {'min': 100, 'max': 200, 'category': 'products', 'fileName': imageFilePath+'blueCirc.png'},

    "battery": {'min': 200, 'max': 200, 'category': 'products', 'fileName': imageFilePath+'battery.png'},
    "gear": {'min': 100, 'max': 100, 'category': 'products', 'fileName': imageFilePath+'gear.png'},

    
    "fish": {'min': 100, 'max': 100, 'category': 'products', 'fileName': imageFilePath+'fish.png'},

    }


#  *** Can't have any weapons in your hands or else the TAB will not work ***
def main():
    SendKey(keys['e']) #Press the 'e' key to open your inventory.

    for itemKey, item in requestedItems.items():
        pya.moveTo(pya.locateOnScreen(imageFilePath + "emptyLogisticsIcon.png", region = (x1,y1,x2,y2))) #Finds and empty square in the personal logistics grid.
        pya.click() #Opens the logistics selection menu

        checkTabSelection(requestedItems[itemKey]['category'])

        if (pya.locateOnScreen(requestedItems[itemKey]['fileName'], region = (x1,y1,x2,y2)) is not None): #Checks to see if it can find the item icon. 
            pya.moveTo(pya.locateOnScreen(requestedItems[itemKey]['fileName'], region = (x1,y1,x2,y2))) #Selects the icon 
            pya.click()
            SendKey(VK_TAB) 
            sendNumbers(requestedItems[itemKey]['min'])
            SendKey(VK_TAB) 
            sendNumbers(requestedItems[itemKey]['max'])
            SendKey(keys['e'])
        else:
            print("Can't find item icon on screen: " + itemKey)


def sendNumbers(num):
    for x in range(len(str(num))):
        strNum = str(num)
        SendKey(keys[strNum[x]])


def checkTabSelection(category): #Checks to make sure the correct tab is selected (logistics, production, products, or weapons)
    if (category == "logistics"):
        #Make sure the logistics tab is selected
        if (pya.locateOnScreen(imageFilePath + "logisticsTabSelected.png") is None): #If it the tab is not selected
            pya.moveTo(pya.locateOnScreen(imageFilePath + "logisticsTabUnselected.png"))
            pya.click()

    elif (category == "production"):
        #Make sure the production tab is selected
        if (pya.locateOnScreen(imageFilePath + "productionTabSelected.png") is None): #If it the tab is not selected
            pya.moveTo(pya.locateOnScreen(imageFilePath + "productionTabUnselected.png"))
            pya.click()

    elif (category == "products"):
        #Make sure the products tab is selected
        if (pya.locateOnScreen(imageFilePath + "productsTabSelected.png") is None): #If it the tab is not selected
            pya.moveTo(pya.locateOnScreen(imageFilePath + "productsTabUnselected.png"))
            pya.click()

    elif (category == "weapons"):
        #Make sure the weapons tab is selected
        if (pya.locateOnScreen(imageFilePath + "weaponsTabSelected.png") is None): #If it the tab is not selected
            pya.moveTo(pya.locateOnScreen(imageFilePath + "weaponsTabUnselected.png"))
            pya.click()
        

time.sleep(3)
print("Start") 
main()
print("Done")
