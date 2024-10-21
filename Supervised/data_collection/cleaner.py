import cv2, os, pandas as pd, numpy as np

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

    backgroun_extend = np.zeros((frame.shape[0] + bottom_right_corner[1]+1, frame.shape[1], frame.shape[2]), dtype=np.uint8)
    backgroun_extend[bottom_right_corner[1]+1:, :] = frame
    frame = backgroun_extend

    cv2.rectangle(frame, top_left_corner, bottom_right_corner, (255, 255, 255), -1)  
    cv2.putText(frame, text, org, fontFace, fontScale, color, thickness)

    return frame

# Base path to the data folder
base_data_path = 'Supervised/data'

# List all the folders in the base directory
folders = [f for f in os.listdir(base_data_path) if os.path.isdir(os.path.join(base_data_path, f))]

# Initialize an empty DataFrame to store all the data
combined_df = pd.DataFrame()

# Loop through each folder
for folder in folders:
    folder_path = os.path.join(base_data_path, folder)
    
    # Load the CSV file
    csv_file = os.path.join(folder_path, 'controls.csv')
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        
        # Add a new column for the image path
        df['image_path'] = df.index.map(lambda i: os.path.join(folder_path, f'frame_{i}.jpg'))
        
        # Combine with the main DataFrame
        combined_df = pd.concat([combined_df, df], ignore_index=True)

clean_df = pd.DataFrame()
indexes = combined_df.columns
print(indexes)
print(combined_df.head())

for i,image_data in combined_df.iterrows():
    image = cv2.imread(image_data['image_path'])
    if image is None:
        print("Error: No image at path -", image_data['image_path'])
    else:
        image = text_on_frame(",".join(t+'='+str(image_data[t]) for t in indexes[1:-1]), image)
        cv2.imshow("Loaded Image", image)

        key = cv2.waitKey(0)
        if key == 's':
            clean_df = pd.concat([clean_df, image_data], ignore_index=True)

clean_df.to_csv('clean_controls.csv', index=False)
cv2.destroyAllWindows()
