#!/usr/bin/env python3
import json
from pathlib import Path
from PIL import Image

import numpy as np
from joblib import dump, load
import json

import torch
from ultralytics import YOLO

from PIL import Image

import numpy as np
import pandas as pd
import glob

import torch
torch.backends.cudnn.benchmark = False
# torch.backends.cudnn.enabled = False

import torchvision.models as models
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data.dataset import Dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import timm
import math

lbl = load("lbl.pkl")

class Ai4SNet(nn.Module):
    def __init__(self):
        super(Ai4SNet, self).__init__()    
        self.model = timm.create_model('efficientnet_b0', num_classes=len(lbl.classes_), pretrained=False)
        
    def forward(self, img, labels=None):        
        feat = self.model(img)
        return feat

class AI4sDataset(Dataset):
    def __init__(self, img_path, img_boxes, transform):
        self.img_path = img_path
        self.img_boxes = img_boxes
        self.transform = transform

    def __getitem__(self, index):
        img = Image.open(self.img_path).convert('RGB')
        
        x, y, w, h = self.img_boxes[index]

        left = x
        top = y
        right = x + w
        bottom = y + h
        img = img.crop((left, top, right, bottom))
        
        if self.transform is not None:
            img = self.transform(img)
        
        return img

    def __len__(self):
        return len(self.img_boxes)

def main():
    input_dir = Path("/saisdata")
    output_file = Path("/saisresult/prediction.json")

    # input_dir = Path("./demo/")
    # output_file = Path("./prediction.json")

    model1 = YOLO("./detect.pt")
    
    model2 = Ai4SNet()
    model2.load_state_dict(torch.load("cls.pt", map_location=torch.device('cpu')))
    model2.eval()
    
    id2label = json.load(open("ID_to_chinese.json"))
    
    results_json = {}
    for img_path in sorted(input_dir.glob("*.png")):
        results = model1.predict(img_path)
        boxes = results[0].boxes.xywh.data.cpu().numpy().astype(int)
        
        dataset = AI4sDataset(
            img_path, 
            boxes,
            transforms.Compose([
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        )
        
        image_id = img_path.stem
        # TODO: 模型推理代码
        # results[image_id] = [
        #     {"bbox": [843, 2087, 93, 89], "text": "天"}
        # ]

        results_json[image_id] = []
        for i in range(len(dataset)):
            text = id2label[lbl.inverse_transform([model2(dataset[i].reshape(1, 3, 128, 128))[0].argmax()])[0]]
            results_json[image_id].append({
                "bbox": list([int(x) for x in boxes[i]]),
                "text": text
            })
            print(image_id, list(boxes[i]), text)
        

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_json, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()