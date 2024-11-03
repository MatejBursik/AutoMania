"""
30-140 left,forward 111

--- format
frame,left,right,forward,backward
frame_0.jpg,0,0,0,0
"""
import pandas as pd

inputs = [
    [[30, 140], [1, 0, 1, 0], 3]
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
