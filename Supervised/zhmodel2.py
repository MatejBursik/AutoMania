from fastai.vision.all import *
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import resnet50

# Load the labels CSV
labels_df = pd.read_csv('C:\\Users\\alame\\Desktop\\pro edition\\deep learning\\AutoMania\\Supervised\\data\\track2\\controls.csv')

# Path to images
path = Path('C:\\Users\\alame\\Desktop\\pro edition\\deep learning\\AutoMania\\Supervised\\data\\track2')

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
    item_tfms=Resize((395, 222)),  # Resize images
    batch_tfms=aug_transforms(  # Apply augmentations during training
        do_flip=True,                # Allow flipping to simulate left-right turns
        flip_vert=False,             # Do not flip vertically as it's irrelevant for driving
        max_rotate=20.0,             # Allow random rotation up to 20 degrees to simulate slight turns
        max_zoom=1.2,                # Allow zoom in/out to simulate different distances
        max_lighting=0.4,            # Vary brightness/contrast to simulate lighting changes
        max_warp=0.2                 # Apply slight perspective warp to simulate shifts
    )
)

# Create DataLoaders
dls = dblock.dataloaders(labels_df, bs=8)

# Define the CNN + LSTM model
class ResNetLSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Load a pretrained ResNet50 model
        self.resnet = resnet50(weights='IMAGENET1K_V1')
        # Remove the last fully connected layer of ResNet50
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-1])
        # LSTM to capture temporal dependencies
        self.lstm = nn.LSTM(input_size=2048, hidden_size=512, num_layers=2, batch_first=True)
        # Fully connected layer for final prediction
        self.fc = nn.Linear(512, 3)  # Predicting steering, throttle, brake
        
    def forward(self, x):
        # Expecting input of shape (batch_size, C, H, W)
        batch_size, C, H, W = x.size()
        
        # Extract features from the image using ResNet50
        frame_features = self.resnet(x)  # Shape: (batch_size, 2048, 1, 1)
        frame_features = frame_features.view(batch_size, 1, -1)  # Shape: (batch_size, 1, 2048)
        
        # Pass through LSTM
        lstm_out, _ = self.lstm(frame_features)  # Shape: (batch_size, 1, 512)
        
        # Take the output of the LSTM cell
        output = lstm_out[:, -1, :]  # Shape: (batch_size, 512)
        
        # Fully connected layer to get final prediction
        output = self.fc(output)  # Shape: (batch_size, 3)
        
        return output

if __name__ == "__main__":
    # Create a Learner object for training the custom model
    model = ResNetLSTMModel()
    loss_func = nn.MSELoss()
    learn = Learner(dls, model, loss_func=loss_func, metrics=[rmse])

    print("Training the model")
    # Train the model for a few epochs
    learn.unfreeze()  # Unfreezing the model to allow fine-tuning of all layers
    learn.fit_one_cycle(10, slice(1e-5, 1e-3))  # Using a range of learning rates for better fine-tuning

    # Evaluate the model on the validation set
    print("Evaluating the model")
    learn.validate()

    # Save the entire model for future use
    learn.export('trackmania4_lstm_learner.pkl')


