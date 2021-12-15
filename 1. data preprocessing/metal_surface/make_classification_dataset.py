import os
import shutil
import json
import cv2

# 오류 라벨이 하나만 있는 이미지
def main():
    data_root = 'C:\\Users\\user\\Desktop\\AIHub data\\2. metal_damaged\\images'
    save_root_img = 'C:\\Users\\user\\Desktop\\AIHub data zip\\2. metal_damaged_classification'
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
        labels = []
        annos = json_data[filename]['anno']
        for anno in annos:
            labels.append(anno['label'])
        labels = set(labels)
        if len(labels) == 1:
            is_mixed = False
        else:
            is_mixed = True

        if not is_mixed: # 이미지 사용!
            label = list(labels)[0]
            img_path = path_list[filename]
            # img_path = os.path.join(data_root, label, filename)
            # if not os.path.isfile(img_path):
            #     break

            # if label == 'waist_folding':
            #     label = 'crease'
            # elif label == 'crease':
            #     label = 'waist_folding' # water_spot   inclusion   oil_spot   silk_spot   punching_hole   rolled_pit
            # # elif: label == 'wel'
            #
            # if filename == 'img_06_4403068300_01280.jpg':
            #     label = 'welding_line'


            save_path = os.path.join(save_root_img, label)
            os.makedirs(save_path, exist_ok=True)
            save_path = os.path.join(save_path, filename)
            try:
                shutil.copy2(img_path, save_path)
            except:
                print(save_path)




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