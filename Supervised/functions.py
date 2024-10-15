import cv2, numpy as np, pyautogui as pg, keyboard, pygetwindow as gw
from fastai.vision.all import *
from pynput.keyboard import Controller, Key
keyboard_controller = Controller()

def process_result(result):
    """
    - result is the answere of the neural network where 0 = up, 1 = down, 2 = left, 3 = right
    - create keyboard input based on the result
    """

    for i,v in enumerate(result[0]):
        if v > 0.8 :
            print(i, round(v, 3), 'start')
            match i:
                case 0:
                    if v < 0:
                        keyboard_controller.press(Key.left)
                    elif v > 0:
                        keyboard_controller.press(Key.right)
                case 1:
                    keyboard_controller.press(Key.up)
                case 2:
                    keyboard_controller.press(Key.down)
        elif v < -0.8:
            print(i, round(v, 3), 'start')
            match i:
                case 0:
                    if v < 0:
                        keyboard_controller.press(Key.left)
                    elif v > 0:
                        keyboard_controller.press(Key.right)
        else:
            print(i, round(v, 3), 'end')
            match i:
                case 0:
                    if v < 0:
                        keyboard_controller.release(Key.left)
                    elif v > 0:
                        keyboard_controller.release(Key.right)
                case 1:
                    keyboard_controller.release(Key.up)
                case 2:
                    keyboard_controller.release(Key.down)

    print()

def get_window_info(title):
    window = gw.getWindowsWithTitle(title)

    if window:
        # get the first matching window
        app_window = window[0]
        
        # get window position and resolution
        pos = (app_window.left, app_window.top)
        res = (app_window.width, app_window.height)
        return (pos, res)

    return None


def take_a_screenshot(title):
    """
    - take a screenshot of the window with the specified title
    - return a numpy array
    """
    win_pos, res = get_window_info(title)
    img = pg.screenshot(region=(win_pos[0], win_pos[1], res[0], res[1]))

    # process the screenshot
    screen = np.array(img)
    screen = cv2.resize(screen, (0, 0), fx = 0.5, fy = 0.5) # down scale by half
    screen = screen[17:-5, 5:-5] # removing unwanted edges
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR) # color correct
    
    return screen



