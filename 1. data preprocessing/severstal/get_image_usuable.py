import cv2
import numpy as np
import os
import json
import shutil


def main():
    image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\5. steel_damaged\\images'
    save_root = 'C:\\Users\\user\\Desktop\\AIHub data zip\\5. steel_damaged\\image'

    json_path = 'C:\\Users\\user\\Desktop\\AIHub data zip\\5. steel_damaged\\anno\\annotation.json'

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    filename_list = {}
    img_paths = get_img_paths(image_root)
    for img_path in img_paths:
        filename = os.path.basename(img_path)
        filename_list[filename] = img_path

    for filename in json_data.keys():
        image_path = filename_list[filename]
        save_path = os.path.join(save_root, filename)
        shutil.copy2(image_path, save_path)



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

if __name__ == '__main__':
    main()