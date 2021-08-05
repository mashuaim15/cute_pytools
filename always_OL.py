import pyautogui
# import os
# os.system('pip install pyautogui')    # auto pip install this package
# pyautogui.dragTo(100, 150)
# pyautogui.dragRel(0, 10)              # drag mouse 10 pixels down
# pyautogui.moveRel(0, 50)              # move mouse 10 pixels down

import os

os.environ['DISPLAY'] = ':0'

def move_mouse():
    pyautogui.moveTo(1600, 150)
    position_v = 150
    position_h = 1600
    for i in range(8):     # move mouse down
        position_v =+ 100
        pyautogui.moveRel(0, position_v, duration=0.5)
    for i in range(10):    # move mouse left
        position_h =- 120
        pyautogui.moveRel(position_h, 0, duration=0.5)
    for i in range(8):    # move mouse up
        position_v =- 100
        pyautogui.moveRel(0, position_v,duration=0.5)
    for i in range(10):    # move mouse right
        position_h =+ 120
        pyautogui.moveRel(position_h, 0,duration=0.5)
    

if __name__ == '__main__':
    move_mouse()