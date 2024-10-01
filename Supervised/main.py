from functions import *

title = "Trackmania"
run = False

while not run:
    if keyboard.is_pressed('shift'): # start recording by 'shift'
        run = True
        print("Started AutoMania ...")

while run:
    if keyboard.is_pressed('ctrl'): # end recording by 'ctrl'
        break
    screen = take_a_screenshot(title)
    result = decision(screen)
    process_result(result)