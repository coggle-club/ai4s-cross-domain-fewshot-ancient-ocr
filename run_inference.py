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

def main():
    input_dir = Path("/saisdata")
    output_file = Path("/saisresult/prediction.json")

    # input_dir = Path("./demo/")
    # output_file = Path("./prediction.json")

    model1 = YOLO("./detect.pt")
        
    results_json = {}
    for img_path in sorted(list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg"))):
        results = model1.predict(img_path)
        boxes = results[0].boxes.xywh.data.cpu().numpy().astype(int)
        cls_ids = results[0].boxes.cls  # Class IDs
        cls_names = [results[0].names[int(id)] for id in cls_ids]  # Class names
        
        image_id = img_path.stem
        # TODO: 模型推理代码
        # results[image_id] = [
        #     {"bbox": [843, 2087, 93, 89], "text": "天"}
        # ]

        results_json[image_id] = []
        for xywh, label in zip(boxes, cls_names):
            results_json[image_id].append({
                "bbox": list([int(x) for x in xywh]),
                "text": label
            })
            print(image_id, xywh, label)
        

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_json, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()