import cv2, numpy as np, pyautogui as pg, keyboard, json, pygetwindow as gw, base64, time, os, pandas as pd

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

# Create a folder to save the images and the CSV
data_folder = 'Supervised/data/training16'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
csv_file = os.path.join(data_folder, 'controls.csv')

# Initialize DataFrame for inputs
if os.path.exists(csv_file):
    controls_df = pd.read_csv(csv_file)
else:
    controls_df = pd.DataFrame(columns=['frame', 'steering', 'throttle', 'brake'])

title = "Trackmania"
win_pos, res = get_window_info(title)
frame_count = 0
keys = ['up', 'down', 'left', 'right']

print(win_pos, res)
run = False

# Wait for the user to start recording by pressing 'shift'
while not run:
    if keyboard.is_pressed('shift'):  # Start recording with 'shift'
        run = True
        print("Recording started ...")

start = time.time()

while run:
    # Take a screenshot of the game
    win_pos = get_window_info(title)[0]
    img = pg.screenshot(region=(win_pos[0], win_pos[1], res[0], res[1]))

    # Process the screenshot
    frame = np.array(img)
    frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)  # Downscale by half
    frame = frame[100:-50, 5:-5]  # Remove unwanted edges
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Color correction

    # Calculate the steering, throttle, and brake values based on key inputs
    steering = 0  # Neutral steering
    throttle = 0  # No throttle
    brake = 0  # No brake

    pressed_keys = [key for key in keys if keyboard.is_pressed(key)]

    if 'left' in pressed_keys:
        steering = -1  # Full left
    elif 'right' in pressed_keys:
        steering = 1  # Full right
    
    if 'up' in pressed_keys:
        throttle = 1  # Full throttle
    
    if 'down' in pressed_keys:
        brake = 1  # Full brake

    # Stop recording when 'ctrl' is pressed
    if keyboard.is_pressed('ctrl'):
        run = False

    # Append control data to the DataFrame
    new_df = pd.DataFrame({
        'frame': [f'frame_{frame_count}.jpg'],
        'steering': [steering],
        'throttle': [throttle],
        'brake': [brake]
    })
    controls_df = pd.concat([controls_df, new_df], ignore_index=True)

    # Save the frame as an image
    frame_filename = os.path.join(data_folder, f'frame_{frame_count}.jpg')
    cv2.imwrite(frame_filename, frame)
    
    frame_count += 1
end = time.time()

print("Recording ended")
print("Number of frames:", frame_count)
print("Time of recording:", end - start)
print("Saving files ...")

controls_df.to_csv(csv_file, index=False)
print("Files saved")