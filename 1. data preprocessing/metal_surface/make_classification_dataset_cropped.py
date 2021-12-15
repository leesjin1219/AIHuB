import os
import shutil
import json
import cv2

# 오류 위치만 크롭한 이미지
# https://blog.perceptilabs.com/use-case-defect-detection-in-metal-surfaces/
def main():
    data_root = 'C:\\Users\\user\\Desktop\\AIHub data\\2. metal_damaged\\images'
    save_root_img = 'C:\\Users\\user\\Desktop\\AIHub data zip\\2. metal_damaged_classification_cropped'
    os.makedirs(save_root_img, exist_ok=True)
    json_path = 'C:\\Users\\user\\Desktop\\AIHub data zip\\2. metal_damaged_detection\\anno\\annotation.json'

    img_paths = get_img_paths(data_root)
    path_list = {}
    for img_path in img_paths:
        filename = os.path.basename(img_path)
        path_list[filename] = img_path

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    for filename in json_data.keys():
        annos = json_data[filename]['anno']
        img_path = path_list[filename]
        img = cv2.imread(img_path)
        for idx, anno in enumerate(annos):
            label = anno['label']
            save_path = os.path.join(save_root_img, label)
            os.makedirs(save_path, exist_ok=True)

            filename_new = filename.split('.')[0] + f'_{idx}.jpg'
            save_path = os.path.join(save_path, filename_new)

            bbox = anno['bbox']
            img_cropped = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]

            cv2.imwrite(save_path, img_cropped)



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