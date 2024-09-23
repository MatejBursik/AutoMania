import cv2, numpy as np, pyautogui as pg, keyboard, json, pygetwindow as gw, base64, time

def text_on_frame(text, frame):
    org = (0, 20)  # bottom-left corner of the text
    fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL
    fontScale = 1
    color = (0, 0, 0)
    thickness = 2

    # calculate and draw the size of the text box
    (text_width, text_height), baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    top_left_corner = (org[0], org[1] - text_height - baseline)
    bottom_right_corner = (org[0] + text_width, org[1] + baseline)
    cv2.rectangle(frame, top_left_corner, bottom_right_corner, (255, 255, 255), -1)  

    # add the text
    cv2.putText(frame, text, org, fontFace, fontScale, color, thickness)

    return frame

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

out_json = {
            'key_inputs' : [],
            'frames' : []
            }

title = "Trackmania"
win_pos, res = get_window_info(title)
keys = ['up', 'down', 'left', 'right']
run = False
print(win_pos, res)

while not run:
    if keyboard.is_pressed('shift'): # start recording by 'shift'
        run = True
        print("Recording started ...")

start = time.time()
while run:
    # take a screenshot of the game
    win_pos = get_window_info(title)[0]
    img = pg.screenshot(region=(win_pos[0], win_pos[1], res[0], res[1]))

    # process the screenshot
    frame = np.array(img)
    frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5) # down scale by half
    frame = frame[17:-5, 5:-5] # removing unwanted edges
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # color correct

    # record the keys pressed during the screenshot
    pressed_keys = [key for key in keys if keyboard.is_pressed(key)]
    
    if keyboard.is_pressed('ctrl'): # end recording by 'ctrl'
        run = False

    # update out_json
    _, encoded = cv2.imencode('.jpg', frame)
    out_json['frames'].append(base64.b64encode(encoded).decode('utf-8'))
    out_json['key_inputs'].append(pressed_keys)
end = time.time()

print("Recording ended")
print("Number of frames:", len(out_json['frames']))
print("Time of recording:", end - start)
print("Saving files ...")

# make out_vid.mp4
fps = len(out_json['frames'])/(end - start)
res = (frame.shape[1], frame.shape[0])
out_vid = cv2.VideoWriter("out_vid.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, res)

for i, frame in enumerate(out_json['frames']):
    encoded = base64.b64decode(frame)
    frame = np.frombuffer(encoded, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    if len(out_json['key_inputs'][i])>0:
        frame = text_on_frame(", ".join(out_json['key_inputs'][i]), frame)
    out_vid.write(frame)

out_vid.release()

# make out_json.json
with open('out_json.json', 'w') as f:
    json.dump(out_json, f, indent=4)

print("Files saved")