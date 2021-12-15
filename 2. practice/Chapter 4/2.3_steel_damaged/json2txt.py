import json
import os

import cv2


def main():
    json_path = r'C:\Users\user\Desktop\AIHub data zip\5. steel_damaged\anno\annotation.json'
    save_root = r'C:\Users\user\Desktop\AIHub data zip\5. steel_damaged\labels'
    os.makedirs(save_root, exist_ok=True)

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    for filename in json_data.keys():
        json_image = json_data[filename]

        filename_save = os.path.splitext(filename)[0] + '.txt'
        save_path = os.path.join(save_root, filename_save)
        f = open(save_path, 'w')

        width = json_image['width']
        height = json_image['height']
        bboxs = json_image['anno']
        for bbox in bboxs:
            label_class = 0
            x_center = (bbox[0] + bbox[2]) / 2
            y_center = (bbox[1] + bbox[3]) / 2
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            write = f'{label_class} {x_center/width} {y_center/height} {w/width} {h/height}\n'
            f.write(write)
        f.close()

if __name__ == '__main__':
    main()