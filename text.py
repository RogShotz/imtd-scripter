# Import required packages
import cv2
import pytesseract
import pyautogui
import numpy as np
import time
import my_logging

global wave_count

def find_text(left: int, top: int , right: int, bottom: int):
    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # take a screenshot of the screen and store it in memory, then
    # convert the PIL/Pillow image to an OpenCV compatible NumPy array
    img = pyautogui.screenshot(region=(left, top, right, bottom))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    texts = pytesseract.image_to_string(img)

    #cv2.imshow("Output", img)
    #cv2.waitKey(0)
    return texts


def draw_boxes_on_character(img):
    img_width = img.shape[1]
    img_height = img.shape[0]
    boxes = pytesseract.image_to_boxes(img)
    for box in boxes.splitlines():
        box = box.split(" ")
        character = box[0]
        x = int(box[1])
        y = int(box[2])
        x2 = int(box[3])
        y2 = int(box[4])
        cv2.rectangle(img, (x, img_height - y), (x2, img_height - y2), (0, 255, 0), 1)

        cv2.putText(img, character, (x, img_height -y2), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        
    return img

def find_wave(): # meant to run in a thread that updates every 5 seconds
    global wave_count
    wave_count = -1
    while True:
        current_prestige = my_logging.log_get("prestiges")
        while current_prestige == my_logging.log_get("prestiges"):
            text = find_text(0,20, 200, 100)
            start = text.lower().find("wave")
            end = text.lower().find("\n")
            try:
                wave = int(text[start+5:end]) # +4 to compensate for wave and /s
                if wave > wave_count: # if it got actual input
                    if my_logging.log_get("prestiges"):
                        wave_count = int(wave)
            except:
                pass

        time.sleep(5)
        wave_count = -1
    return