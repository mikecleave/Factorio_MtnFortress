import pyautogui as pya
import time

time.sleep(3)

location = pya.locateOnScreen('img/entityBackgroundColor.png')
print(location)
