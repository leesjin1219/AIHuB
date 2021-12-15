import cv2
import numpy as np
import os
import json
import shutil
from tqdm import tqdm

def main():
    image_root = r'C:\Users\user\Desktop\data\6. airport_xray\images'
    save_root = r'C:\Users\user\Desktop\data\6. airport_xray\images_jpg'

    img_paths = get_img_paths(image_root)
    for img_path in img_paths:
        datatype = img_path.split('\\')[-2]
        filename = os.path.basename(img_path)
        filename_new = os.path.splitext(filename)[0] + '.jpg'
        image = cv2.imread(img_path)
        save_path = os.path.join(save_root, datatype)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, filename_new)
        cv2.imwrite(save_path, image)


def get_img_paths(root_path):
    img_paths = []
    for (path, dir, files) in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng']
            if ext in formats:
                img_path = os.path.join(path, file)
                img_paths.append(img_path)
    return img_paths

def get_xml_paths(root_path):
    img_paths = []
    for (path, dir, files) in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            formats = ['.xml']
            if ext in formats:
                img_path = os.path.join(path, file)
                img_paths.append(img_path)
    return img_paths

if __name__ == '__main__':
    main()