# game must be windowed with windows bar below, on  a 1920x1080 screen to work
# start without anything on board

import pyautogui
import time
import random
import my_logging as log
import threading
import text
from queue import Queue

# consts
pyauto_pause = 0.1

pyautogui.FAILSAFE = True
pyautogui.PAUSE = pyauto_pause

debug_mode = False
dev_mode = False

# code related vars
monster_position = []
fncqueue = Queue(maxsize = 0)


# INTERNAL FNC AREA

# click obfuscation, adds a random value +-3 pixels in any direction
def click_obf(location: object):
    point = pyautogui.center(location)
    x_offset = random.randint(-3, 3)
    y_offset = random.randint(-3, 3)
    pyautogui.moveTo(point.x+x_offset, point.y +
                     y_offset, .5, pyautogui.easeInQuad)
    pyautogui.click(point.x+x_offset, point.y+y_offset)
    log.log_add("clicks")


# xy counterpart
def click_obf_xy(x: int, y: int):
    x_offset = random.randint(-3, 3)
    y_offset = random.randint(-3, 3)
    pyautogui.moveTo(x+x_offset, y+y_offset, .5, pyautogui.easeOutQuad)
    pyautogui.click(x+x_offset, y+y_offset)
    log.log_add("clicks")


# INIT AREA

def macro_init():
    boss_rush()  # ensures boss rush is on
    boss_rush()  # needs two, one to refocus, on to actually start
    loadout()    # load loadout, to make sure someone didnt forget i.e. (me)
    play(True)   # start off running

    # thread bootup
    detector_thread = threading.Thread(target=detector)
    detector_thread.start()

    wave_thread = threading.Thread(target=text.find_wave)
    wave_thread.start()



def map_pos_init():  # TODO: Proof this

    # find all circles
    global monster_position
    monster_position = pyautogui.locateAllOnScreen(
        'BUTTON.PNG', confidence=0.8)

# THREADING SECTION FOR DETECTION

def detector():
    while True:
        global fncqueue
        defeat_found = pyautogui.locateOnScreen(
            'Defeat_Cut.png', confidence=0.8)
        
        if(defeat_found):
            fncqueue.put(auto_prestige)
        
        im = pyautogui.screenshot(region=(1850, 900, 100, 100))
        new_indicator = pyautogui.locate("new_indicator.png", im, confidence=0.4)

        if(new_indicator):
            print("ad detection")
            fncqueue.put(check_ad)
        
        while not fncqueue.empty():
            time.sleep(1)
        time.sleep(1)
        

# GAME MACRO AREA

def auto_prestige():  # running on seperate thread
    prestige_location = pyautogui.locateOnScreen(
        'prestige_cut.png', confidence=0.8)
        
    if prestige_location:
        click_obf(prestige_location)
        prestige_nested_button = pyautogui.locateOnScreen(
            'prestige_button.png', confidence=0.8)
        if not prestige_nested_button:
            print("Defeat Detected, but no Prestige Nested Button")
            print("Attempting to scroll prestige menu")
            nested_map_selection_button_location = pyautogui.locateOnScreen(
                'nested_map_selection_button.png', confidence=0.8)
            if nested_map_selection_button_location:
                # click ensures were in the menu
                click_obf(nested_map_selection_button_location)
                pyautogui.PAUSE = 0
                for i in range(50):
                    pyautogui.scroll(-10)
                    time.sleep(.01)
                pyautogui.PAUSE = pyauto_pause
            else:
                print(
                    "ERR: nested_map_selection_button_location was not found")
        prestige_nested_button = pyautogui.locateOnScreen(
            'prestige_button.png', confidence=0.8)
        if prestige_nested_button:
            click_obf(prestige_nested_button)
            log.log_add("prestiges")
            print(
                f'Prestige Count Up to: {log.log_get("prestiges")}')
            time.sleep(10)
            loadout()
            boss_rush()
            play(True)
        else:
            print("ERR: prestige_nested_button was not")
    else:
                print("ERR: Defeat Detected, but no Prestige Button")
    time.sleep(1)


def play(play: bool):
    play_location = pyautogui.locateOnScreen('play_button.png', confidence=0.8)
    pause_location = pyautogui.locateOnScreen(
        'pause_button.png', confidence=0.8)

    if play_location:  # if the play button exists
        if play:  # and the user wants to play
            click_obf(play_location)
    if pause_location:  # if the pause button exists
        if not play:  # and the user wants to pause
            click_obf(pause_location)

    print(f'play = {play}')


def loadout():
    loadout_button_location = pyautogui.locateOnScreen(
        'loadout_button.png', confidence=0.8)

    if loadout_button_location:
            click_obf(loadout_button_location)
            load_loadout_button_location = pyautogui.locateOnScreen(
                'load_loadout_button.png', confidence=0.7)
            if load_loadout_button_location:  # limited to first instace i.e. Towers1
                click_obf(load_loadout_button_location)
            else:
                print("ERR: load_loadout_button not found")
    else:
        print("ERR: loadout_button not found")


def upgrade(pos: int):
    #def upgrade(pos_list: list):  # TODO: Proof this
    '''
    pix = pyautogui.pixel(1170, 942)
    global monster_position
    if monster_position is empty:  # TODO: empty?
        #map_pos_init()

    for pos in pos_list:
        click_obf_xy(monster_position[pos])
        time.sleep(.15)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(
            1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)

        pyautogui.press('esc')
    '''
    #1st pos
    if pos == 1 or pos ==  0:
        click_obf_xy(879, 185)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)
    #3rd pos
    if pos == 3 or pos == 0:
        click_obf_xy(878, 300)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)

    if pos == 4 or pos == 0:
        click_obf_xy(880, 350)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)
    
    if pos == 5 or pos == 0:
        click_obf_xy(1040, 355)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)

    if pos == 8 or pos == 0:
        click_obf_xy(1040, 520)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)

    if pos == 10 or pos == 0:
        click_obf_xy(1040, 635)
        time.sleep(.1)
        upgrade_button_pixel = pyautogui.pixelMatchesColor(1170, 942, (143, 204, 84))
        if upgrade_button_pixel:
            click_obf_xy(1170, 942)
    
    time.sleep(.1)
    pyautogui.press('esc')

def check_ad():
    click_obf_xy(1890, 950)
    time.sleep(.15)
    pyautogui.press('esc')
    log.log_add("ads")


def autocast(restrict_boss: bool):
    riches_spell_location = pyautogui.locateOnScreen(
        'riches_spell.png', confidence=0.8)
    power_spell_location = pyautogui.locateOnScreen(
        'power_spell.png', confidence=0.8)
    mastership_spell_location = pyautogui.locateOnScreen(
        'mastership_spell.png', confidence=0.8)
    time_spell_location = pyautogui.locateOnScreen(
        'time_spell.png', confidence=0.8)

    if riches_spell_location:
        if restrict_boss:
            if text.wave_count % 5 == 0:
                click_obf(riches_spell_location)
                #print("Boss Spell Casted")
        else:
            click_obf(riches_spell_location)

    if power_spell_location:
        click_obf(power_spell_location)

    if mastership_spell_location:
        if restrict_boss:
            if text.wave_count % 5 == 0:
                click_obf(mastership_spell_location)
                #print("Boss Spell Casted")
        else:
            click_obf(riches_spell_location)

    if time_spell_location:
        click_obf(time_spell_location)


def boss_rush():
    boss_rush_button_location = pyautogui.locateOnScreen(
        'boss_rush_button.png', confidence=0.9)

    if boss_rush_button_location:
        click_obf(boss_rush_button_location)
        print("Boss Rush Enabled")
        # Point
        mini_boss_rush_button_location = pyautogui.locateCenterOnScreen('mini_boss_rush_button.png', confidence=0.8)
        if mini_boss_rush_button_location:
            click_obf_xy(mini_boss_rush_button_location.x+140, mini_boss_rush_button_location.y)


def mob_rush():
    if text.wave_count < 200 and text.wave_count > 0:
        mob_button_location = pyautogui.locateOnScreen(
            'mob_button.png', confidence=0.8)
        if mob_button_location:
            click_obf(mob_button_location)
            mob_begin_button_location = pyautogui.locateOnScreen(
                'mob_begin_button.png', confidence=0.8)
            if mob_begin_button_location:
                click_obf(mob_begin_button_location)
                print(f"MOB RUSH @ WAVE {text.wave_count}")


time.sleep(3)

# trap in dev mode if wanted
while dev_mode:
    print(pyautogui.position())

macro_init()

while True:
    while(not fncqueue.empty()):
        func = fncqueue.get()
        func()
    
    upgrade(8)
    #upgrade(10)
    autocast(True)
    mob_rush()
    time.sleep(2)
