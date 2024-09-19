import cv2, numpy as np, pyautogui as pg, keyboard, json, pygetwindow as gw, time

def text_on_frame(text, frame):
    org = (0, 20)  # Bottom-left corner of the text
    fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL
    fontScale = 1
    color = (0, 0, 0)
    thickness = 2

    # Calculate and draw the size of the text box
    (text_width, text_height), baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    top_left_corner = (org[0], org[1] - text_height - baseline)
    bottom_right_corner = (org[0] + text_width, org[1] + baseline)
    cv2.rectangle(frame, top_left_corner, bottom_right_corner, (255, 255, 255), -1)  

    # Step 5: Add the text on top of the blue rectangle
    cv2.putText(frame, text, org, fontFace, fontScale, color, thickness)

    return frame

def get_window_info(title):
    windows = gw.getAllTitles()
    windows = [win for win in windows if win]
    window = gw.getWindowsWithTitle(title)

    if window:
        # Get the first matching window
        app_window = window[0]
        
        # Get window position and size
        pos = (app_window.left, app_window.top)
        res = (app_window.width, app_window.height)
        return (pos, res)

    return None

win_pos, res = get_window_info("Trackmania")
print(win_pos, res)
fps = 30
keys = ['up', 'down', 'left', 'right']

# outputs
out_vid = cv2.VideoWriter("out_vid.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, res)
out_json = []

run = True
while run:
    # take a screenshot of the game
    win_pos = get_window_info("Trackmania")[0]
    img = pg.screenshot(region=(win_pos[0], win_pos[1], res[0], res[1]))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # record the keys pressed during the screenshot
    pressed_keys = [key for key in keys if keyboard.is_pressed(key)]
    
    if keyboard.is_pressed('esc'):
        run = False

    # update out_json
    """
    out_json.append({
            'frame' : frame.tolist(),
            'key_info' : pressed_keys
            })
    """

    # update out_vid
    if len(pressed_keys)>0:
        frame = text_on_frame(", ".join(pressed_keys), frame)
    out_vid.write(frame)

    time.sleep(1/fps)
        
with open('out_json.json', 'w') as f:
    json.dump(out_json, f)
out_vid.release()
