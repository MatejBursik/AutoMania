from fastai.vision.all import *
import pandas as pd

# Load the labels CSV
labels_df = pd.read_csv('Supervised\\data\\controls.csv')

# Path to images
path = Path('Supervised\\data')

# Define a function to get the control inputs for each image
def get_y(row):
    return tensor([row['steering'], row['throttle'], row['brake']])

def get_x(row):
    return path / row['frame']  # Using '/' for path concatenation

# DataBlock for regression task
dblock = DataBlock(
    blocks=(ImageBlock, RegressionBlock),  # Images as input, continuous labels as output
    get_x=get_x,  # Get image path
    get_y=get_y,  # Get control inputs as a tensor
    splitter=RandomSplitter(valid_pct=0.2),  # Split train/validation
    item_tfms=Resize((395,222)),  # Resize images to 224x224
    batch_tfms=aug_transforms()  # Apply augmentations during training
)
print("a")
# Create DataLoaders
dls = dblock.dataloaders(labels_df)
print("s")
# Define the learner with a pretrained model
learn = vision_learner(dls, resnet34, metrics=accuracy)
print("d")

# Train the model for a few epochs
learn.fine_tune(5)
print("f")
# Evaluate the model on the validation set
learn.validate()

# Export the entire learner (including preprocessing steps)
learn.export('trackmania_learner.pkl')