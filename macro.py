import pyautogui
import time
import random

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

print(random.randint(-3,3))

#click obfuscation, adds a random value +-3 pixels in any direction
def click_obf(location: object):
    point = pyautogui.center(location)
    x_offset = random.randint(-3,3)
    y_offset = random.randint(-3,3)
    print(x_offset)
    print(y_offset)
    pyautogui.click(point.x+x_offset, point.y+y_offset)
    
def auto_prestige():
    defeat_found = pyautogui.locateOnScreen('Defeat_Cut.png', confidence=0.8)
    prestige_location = pyautogui.locateOnScreen('prestige_cut.png', confidence=0.8)

    if defeat_found:
        if prestige_location:
            click_obf(prestige_location)
            prestige_nested_button = pyautogui.locateOnScreen('prestige_button.png', confidence=0.8)
            if prestige_nested_button:
                #click_obf(prestige_nested_button)
                return True
            else:
                print("ERR: Defeat Detected, but no Prestige Nested Button")
        else:
            print("ERR: Defeat Detected, but no Prestige Button")

    print(f'defeat_found = {defeat_found}')
    return False

def play(play: bool):
    play_location = pyautogui.locateOnScreen('play_button.png', confidence=0.8)
    pause_location = pyautogui.locateOnScreen('pause_button.png', confidence=0.8)

    if play_location: # if the play button exists
        if play: # and the user wants to play
            click_obf(play_location)
    if pause_location: # if the pause button exists
        if not play: # and the user wants to pause
            click_obf(pause_location)

    print(f'play = {play}')

def loadout():
    loadout_button_location = pyautogui.locateOnScreen('loadout_button.png', confidence=0.8)

    if loadout_button_location:
        loadout_button_point = pyautogui.center(loadout_button_location)
        pyautogui.click(loadout_button_point.x, loadout_button_point.y)
        load_loadout_button_location = pyautogui.locateOnScreen('load_loadout_button.png', confidence=0.8)
        if load_loadout_button_location: # limited to first instace i.e. Towers1
            load_loadout_button_point = pyautogui.center(load_loadout_button_location)
            pyautogui.click(load_loadout_button_point.x, load_loadout_button_point.y)
    else:
        print("ERR: loadout_button not found")

while True:
    if auto_prestige():
        time.sleep(10)
        loadout()
        play(True)
    time.sleep(1)

