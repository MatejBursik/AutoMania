"""
0-205 forward 205
225-370 right,forward 145
410-465 forward 55
475-575 left,forward 100
630-638 forward 8
645-665 forward 20
845-973 forward 128

left - 101
right - 161
forward - 421

vertical flip = 247 in left/right
double = 494

left/right - 494
forward - 421
all - 915

--- format
frame,left,right,forward,backward
frame_0.jpg,0,0,0,0
"""
import pandas as pd

inputs = [
    [[0, 205], [0, 0, 1, 0], 1],
    [[225, 370], [0, 1, 1, 0], 2],
    [[410, 465], [0, 0, 1, 0], 1],
    [[475, 575], [1, 0, 1, 0], 2],
    [[630, 638], [0, 0, 1, 0], 1],
    [[645, 665], [0, 0, 1, 0], 1],
    [[845, 973], [0, 0, 1, 0], 1]
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
