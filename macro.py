# game must be windowed with windows bar below, at 1920x1080 to work

import pyautogui
import time
import random
import my_logging as log

pyauto_pause = 0.01

pyautogui.FAILSAFE = True
pyautogui.PAUSE = pyauto_pause

debug_mode = False
dev_mode = False

#click obfuscation, adds a random value +-3 pixels in any direction
def click_obf(location: object):
    point = pyautogui.center(location)
    x_offset = random.randint(-3,3)
    y_offset = random.randint(-3,3)
    #print(f'loc click at: {point.x+x_offset}, {point.y+y_offset}')
    pyautogui.moveTo(point.x+x_offset, point.y+y_offset, 1, pyautogui.easeInQuad)
    pyautogui.click(point.x+x_offset, point.y+y_offset)
    log.log_add("clicks")

def click_obf_xy(x: int, y:int):
    x_offset = random.randint(-3,3)
    y_offset = random.randint(-3,3)
    #print(f'xy click at: {x+x_offset}, {y+y_offset}')
    pyautogui.moveTo(x+x_offset, y+y_offset, 1, pyautogui.easeOutQuad)
    pyautogui.click(x+x_offset, y+y_offset)
    log.log_add("clicks")
    
def auto_prestige():
    defeat_found = pyautogui.locateOnScreen('Defeat_Cut.png', confidence=0.8)
    prestige_location = pyautogui.locateOnScreen('prestige_cut.png', confidence=0.8)

    if defeat_found:
        if prestige_location:
            click_obf(prestige_location)
            prestige_nested_button = pyautogui.locateOnScreen('prestige_button.png', confidence=0.8)
            if not prestige_nested_button:
                print("Defeat Detected, but no Prestige Nested Button")
                print("Attempting to scroll prestige menu")
                nested_map_selection_button_location = pyautogui.locateOnScreen('nested_map_selection_button.png', confidence=0.8)
                if nested_map_selection_button_location:
                    click_obf(nested_map_selection_button_location) # click ensures were in the menu
                    pyautogui.PAUSE = 0
                    for i in range(50):
                        pyautogui.scroll(-10)
                        time.sleep(.01)
                    pyautogui.PAUSE = pyauto_pause
                else:
                    print("ERR: nested_map_selection_button_location was not found")
            prestige_nested_button = pyautogui.locateOnScreen('prestige_button.png', confidence=0.8)
            if prestige_nested_button:
                click_obf(prestige_nested_button)
                return True
            else:
                print("ERR: prestige_nested_button was not")
        else:
            print("ERR: Defeat Detected, but no Prestige Button")

    #print(f'defeat_found = {defeat_found}')
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
        click_obf(loadout_button_location)
        load_loadout_button_location = pyautogui.locateOnScreen('load_loadout_button.png', confidence=0.8)
        if load_loadout_button_location: # limited to first instace i.e. Towers1
            click_obf(load_loadout_button_location)
    else:
        print("ERR: loadout_button not found")

def upgrade(pos: int): #TODO: make better with vars and image scraping
    #1st pos
    if pos == 1 or pos ==  0:
        click_obf_xy(879, 185)
        click_obf_xy(1170, 942)
    #3rd pos
    if pos == 3 or pos == 0:
        click_obf_xy(878, 298)
        click_obf_xy(1170, 942)
    pyautogui.press('esc')

def check_ad():
    if not pyautogui.pixelMatchesColor(1890, 950, (0, 0, 0)): # finds if pixel at location is black
        print("ad detected")
        click_obf_xy(1890, 950)
        pyautogui.press('esc')
    else:
        print("ad not detected")

def autocast():
    riches_spell_location = pyautogui.locateOnScreen('riches_spell.png', confidence=0.8)
    power_spell_location = pyautogui.locateOnScreen('power_spell.png', confidence=0.8)
    mastership_spell_location = pyautogui.locateOnScreen('mastership_spell.png', confidence=0.8)
    time_spell_location = pyautogui.locateOnScreen('time_spell.png', confidence=0.8)

    if riches_spell_location:
        click_obf(riches_spell_location)
    
    if power_spell_location:
        click_obf(power_spell_location)
    
    if mastership_spell_location:
        click_obf(mastership_spell_location)
    
    if time_spell_location:
        click_obf(time_spell_location)
    

time.sleep(3)
play(True) #start off running
play(True) #needs two, one to refocus, on to actually start

loop_count = 0
while True:
    if dev_mode:
        print(pyautogui.position())
        time.sleep(.1)
    else:
        if auto_prestige():
            log.log_add("prestiges")
            print(f'Prestige Count Up to: {log.log_get("prestiges")}')
            time.sleep(10)
            loadout()
            play(True)
        upgrade(0)
        autocast()
        if loop_count % 60 == 0: # check every 60 ticks
            check_ad()
        time.sleep(1)
        loop_count += 1

