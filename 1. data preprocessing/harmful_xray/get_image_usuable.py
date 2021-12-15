import cv2
import numpy as np
import os
import json
import shutil
from tqdm import tqdm

def main():
    json_path = 'C:\\Users\\user\\Desktop\\AIHub data zip\\6. airport_xray\\anno\\annotation.json'

    image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\6. airport_xray\\Smith'
    save_root = 'C:\\Users\\user\\Desktop\\AIHub data zip\\6. airport_xray\\image'
    os.makedirs(save_root, exist_ok=True)

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    filename_list = {}
    img_paths = get_img_paths(image_root)
    for img_path in img_paths:
        filename = os.path.basename(img_path)
        filename_list[filename] = img_path

    for filename in json_data.keys():
        image_path = filename_list[filename]
        # C:\Users\user\Desktop\AIHub data\6. airport_xray\Smith\Knife\Single_Other\H_8211.91-0000_01_001.png
        label, image_type = image_path.split('\\')[-3], image_path.split('\\')[-2]

        save_path = os.path.join(save_root, label, image_type)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, filename)

        shutil.copy2(image_path, save_path)



def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

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