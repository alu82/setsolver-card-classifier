# SET card classifier
Classifier for classifying the 81 cards of the game SET (https://www.amigo-spiele.de/spiel/set). 

## The dataset

### Get the pictures
I took the images manually with my smartphone
- color by color (27 cards each picture)
- from different angles
- with daylight (dataset might be enhanced with other light conditions)

### Cut the cards
Afterwards I cut the cards manually with Shutter (https://shutter-project.org/)
- set a predefined size of the screenshot
- I moved this rectangle around to cut each single card
- After pressing enter the card has automatically been saved

### Sort cards into folder structure
With a script (img_generate_folders.py) I created the folder structure and then sorted the card pictures manually (uff).

### Image preprocessing
Since I used Shutter only for the second half of the pictures, I had images with different sizes. The script img_normalize_images.py normalizes them, so that every image in a given folder has the same size. 
- Image is first stretched, without loosing parts of the original image
- Afterwards it is positioned in the middle of the normalized image
- The borders (horizontally or vertically) are black

The size of the normalized images is 
```
img_height = 250
img_width = 160
```

### Transforms
#### Create syntetic images
The dataset with 8 images each card is very small
- 7 images for training (with 1 duplicate for a standard card to get a good balance, so 6 different images)
- 1 image for testing (a standard image with the card taken from the top)

Therefore during training transforms are used
- to rotate the image a bit
- to change the perspective

Don't flip the cards, because the "wave cards" are not symetric.

#### Normalize
It is very important to normalize the image values. I used a python script to get the values for mean and standard deviation for my dataset (unfortunatly i lost the link).

## The neural network

The neural network is a combination of convolutional and fully connected layers. 
```
SetCardClassifier(
  (conv1): Conv2d(3, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (conv2): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (conv3): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (conv4): Conv2d(64, 128, kernel_size=(5, 5), stride=(1, 1), padding=(1, 1))
  (conv5): Conv2d(128, 256, kernel_size=(5, 5), stride=(1, 1), padding=(1, 1))
  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (fc1): Linear(in_features=4608, out_features=1024, bias=True)
  (fc2): Linear(in_features=1024, out_features=256, bias=True)
  (fc3): Linear(in_features=256, out_features=81, bias=True)
  (dropout): Dropout(p=0.5, inplace=False)
)
```
For more details and how the layers are connected see the Jupyter notebook.

## Training the network

- standard process applied when training a pytorch model
- save the model with the lowest validation loss (not accuracy!)

## Trained models

| Modelname | Epochs | Dropout | batch size | learn rate | Val acc | Test acc | 
| --------- | ------ | ------- | ---------- | ---------- | ------- | -------- |
| model_01  | 2500   | 0.5     | 4          | 0.0003     | 1.000   | 1.000    |
| model_02  | 300    | 0.5     | 4          | 0.0003     | 0.965   | 1.000    |


## sources of inspiration

https://towardsdatascience.com/detecting-set-cards-using-transfer-learning-b297dcf3a564

https://medium.com/swlh/image-classification-for-playing-cards-26d660f3149e


