import os
import glob
import cv2
import numpy as np

base_folder = f"{os.path.dirname(__file__)}/images"
folders = ["train", "test"]
img_height = 250
img_width = 160

def normalize_image(img):
    norm_img = scale_image(img)
    norm_img = embed_in_std_img(norm_img)
    return norm_img
    
def scale_image(img):
    h, w, _ = img.shape
    scale_factor = min(img_height/h, img_width/w)
    nh, nw = int(scale_factor*h), int(scale_factor*w)
    scaled_img = cv2.resize(img, (nw, nh), interpolation = cv2.INTER_AREA)
    return scaled_img

def embed_in_std_img(img):
    std_img = np.zeros([img_height,img_width,3],dtype=np.uint8)
    h, w, _ = img.shape
    yoff = round((img_height-h)/2)
    xoff = round((img_width-w)/2)
    std_img[yoff:yoff+h, xoff:xoff+w] = img
    return std_img

for folder in folders:
    imgs_folder = f"{base_folder}/{folder}/"
    for img_folder in glob.glob(imgs_folder + "*"):
        for img_path in glob.glob(img_folder + "/*.png"):
            img = cv2.imread(img_path)
            img = normalize_image(img)
            status = cv2.imwrite(img_path,img)
            print(img_path, status)

