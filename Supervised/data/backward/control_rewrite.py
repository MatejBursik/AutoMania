"""
0-25 backward 26
100-125 backward 26
150-180 backward 31
250-259 backward 10

--- format
frame,left,right,forward,backward
frame_0.jpg,0,0,0,0
"""
import pandas as pd

inputs = [
    [[0, 25], [0, 0, 0, 1], 1],
    [[100, 125], [0, 0, 0, 1], 1],
    [[150, 180], [0, 0, 0, 1], 1],
    [[250, 259], [0, 0, 0, 1], 1]
]
controls_df = pd.DataFrame(columns=['frame', 'left', 'right', 'forward', 'backward'])

for nums,inp,mult in inputs:
    for _ in range(mult):
        for i in range(nums[0], nums[1]+1):
            new_df = pd.DataFrame({
                'frame': [f'frame_{i}.jpg'],
                'left' : inp[0],
                'right' : inp[1],
                'forward' : inp[2],
                'backward' : inp[3]
            })
            controls_df = pd.concat([controls_df, new_df], ignore_index=True)

print(controls_df)
controls_df.to_csv("controls.csv", index=False)
