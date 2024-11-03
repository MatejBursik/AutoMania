import cv2, numpy as np, pyautogui as pg, pygetwindow as gw, time
from fastai.vision.all import *
from pynput.keyboard import Controller, Key
keyboard_controller = Controller()

def process_result(result, toggle):
    sens = 0.5
    press_t = 0.09 # 0.1 struggles up hills, 0.2 basically the same speed as release on next cycle

    bool_result = [v>sens for v in result[0]]
    keys = [Key.left, Key.right, Key.up, Key.down]

    for k,b,v in zip(keys, bool_result, result[0]):
        if b:
            keyboard_controller.press(k)
        if toggle:
            print(str(k)[4:], round(v, 3), b)

    time.sleep(press_t)

    for k in keys:
        keyboard_controller.release(k)

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
    screen = cv2.resize(screen, (400, 225), interpolation=cv2.INTER_LINEAR) # down scale by half
    screen = screen[105:-25, 5:-5] # removing unwanted edges
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR) # color correct
    
    return screen



