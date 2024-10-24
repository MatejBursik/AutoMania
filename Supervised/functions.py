import cv2, numpy as np, pyautogui as pg, pygetwindow as gw
from fastai.vision.all import *
from pynput.keyboard import Controller, Key
keyboard_controller = Controller()

def process_result(result, toggle):
    """
    - result is the answere of the neural network where 0 = steering, 1 = down, 2 = throttle, 3 = brake
    - create keyboard input based on the result
    """
    sens = 0.6
    for i,v in enumerate(result[0]):
        if v > sens :
            print(i, round(v, 3), 'start')
            match i:
                case 0:
                    if v > 0:
                        keyboard_controller.press(Key.right)
                        if toggle:
                            print('steering', round(v, 3), 'on')
                case 1:
                    keyboard_controller.press(Key.up)
                    if toggle:
                        print('throttle', round(v, 3), 'on')
                case 2:
                    keyboard_controller.press(Key.down)
                    if toggle:
                        print('brake', round(v, 3), 'on')
        elif v < -sens:
            match i:
                case 0:
                    if v < 0:
                        keyboard_controller.press(Key.left)
                        if toggle:
                            print('steering', round(v, 3), 'on')
        else:
            match i:
                case 0:
                    keyboard_controller.release(Key.left)
                    keyboard_controller.release(Key.right)
                    if toggle:
                        print('steering', round(v, 3), 'off')
                case 1:
                    keyboard_controller.release(Key.up)
                    if toggle:
                        print('throttle', round(v, 3), 'on')
                case 2:
                    keyboard_controller.release(Key.down)
                    if toggle:
                        print('brake', round(v, 3), 'off')
    if toggle:
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



