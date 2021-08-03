import glob
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

class SetDataSet(Dataset):
    def __init__(self, path, train, transform=None):
        super().__init__()
        self.transform = transform
        self.img_height = 250
        self.img_width = 166
        if train:
            self.imgs_path = f"{path}/train/"
        else:
            self.imgs_path = f"{path}/test/"

        dir_list = glob.glob(self.imgs_path + "*")
        self.data = []
        for card_path in dir_list:
            card_id = int(card_path.split("/")[-1][:2])
            for img_path in glob.glob(card_path + "/*.png"):
                self.data.append([img_path, card_id])

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        img_path, card_id = self.data[index]
        img = cv2.imread(img_path)
        img = self.normalize_image(img)
        if self.transform is not None:
            img = self.transform(img)
        card_id = torch.tensor(card_id)
        return img, card_id

    def normalize_image(self, img):
        norm_img = self.scale_image(img)
        norm_img = self.embed_in_std_img(norm_img)
        return norm_img
    
    def scale_image(self, img):
        h, w, _ = img.shape
        scale_factor = min(self.img_height/h, self.img_width/w)
        nh, nw = int(scale_factor*h), int(scale_factor*w)
        scaled_img = cv2.resize(img, (nw, nh), interpolation = cv2.INTER_AREA)
        return scaled_img
    
    def embed_in_std_img(self, img):
        std_img = np.zeros([self.img_height,self.img_width,3],dtype=np.uint8)
        h, w, _ = img.shape
        yoff = round((self.img_height-h)/2)
        xoff = round((self.img_width-w)/2)
        std_img[yoff:yoff+h, xoff:xoff+w] = img
        return std_img

#path = "/home/aldw/Documents/develop/repos_alu82/set-solver-generate-testdata"
#ds = SetDataSet(path, train=True)
#for idx in range(len(ds)):
#    img, label = ds.__getitem__(idx)

