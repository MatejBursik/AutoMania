import cv2, numpy as np, pyautogui as pg, keyboard, pygetwindow as gw
from fastai.vision.all import *

def process_result(result):
    """
    - result is the answere of the neural network where 0 = up, 1 = down, 2 = left, 3 = right
    - create keyboard input based on the result
    """

    for i,v in enumerate(result):
        if v > 0.7:
            match i:
                case 0:
                    keyboard.press("up")
                case 1:
                    keyboard.press("down")
                case 2:
                    keyboard.press("left")
                case 3:
                    keyboard.press("right")
        else:
            match i:
                case 0:
                    keyboard.release("up")
                case 1:
                    keyboard.release("down")
                case 2:
                    keyboard.release("left")
                case 3:
                    keyboard.release("right")


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


def decision(screen):
    """
    - apply the neural network model onto the screenshot
    - get a decision out of it and store it in result
    """
    # Load the exported learner
    learn = load_learner('trackmania_learner.pkl')

    # Now you can make predictions
    img = PILImage.create('path_to_image.jpg')

    # steering, throttle, brake 
    result = learn.predict(img)

    return result
