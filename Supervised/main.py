from functions import *

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

while not run:
    if keyboard.is_pressed('q'): # start recording by 'q'
        run = True
        print("Started AutoMania ...")

while run:
    if keyboard.is_pressed('e'): # end recording by 'e'
        break
    screen = take_a_screenshot(title)
    result = decision(screen)

    process_result(result)

print("OFF")