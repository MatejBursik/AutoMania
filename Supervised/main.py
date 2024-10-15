from functions import *
import keyboard

def get_y(row):
    return tensor([row['steering'], row['throttle'], row['brake']])

def get_x(row):
    return row['frame']  # Using '/' for path concatenation

def decision(screen):
    """
    - apply the neural network model onto the screenshot
    - get a decision out of it and store it in result
    """
    # Load the exported learner
    learn = load_learner('Supervised/trackmania_learner_fp16.pkl')

    # steering, throttle, brake 
    result = learn.predict(screen)

    return result

print("ON")

title = "Trackmania"
run = False

while True:
    if keyboard.is_pressed('q'): # start driving by 'q'
        run = True
        print("Started AutoMania ...")

    while run:
        if keyboard.is_pressed('e'): # end driving by 'e'
            run = False
        screen = take_a_screenshot(title)
        result = decision(screen)
        process_result(result, True)

    if keyboard.is_pressed('t'): # terminate program by 't'
        break
print("OFF")