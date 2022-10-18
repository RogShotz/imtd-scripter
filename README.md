# IMTD SCRIPTER

## Functionality

PyautoGUI for mouse directing and screen capture

OpenCV and pytesseract for image and text detection for pertaining data

## Code Structure

### Areas
Internal FNC Area: Used for internal helper functions for macro.py

Init Area: For initializing bot, additionally boots up concurrent threads. NEVER manipulate cursor or clicks in thread related structures.

Threading Area: For running thread dependent detectors.

Game Macro Area: Game specific sequencing, detection, and manipulation of mouse/ keyboard inputs for playing the game
