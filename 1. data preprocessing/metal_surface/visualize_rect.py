import os
import json
from xml.etree.ElementTree import parse
import cv2
from tqdm import tqdm

'''
iron_dic = {'1_chongkong': 'punching_hole', '2_hanfeng': 'welding_line', '3_yueyawan': 'crescent_gap',
            '4_shuiban': 'water_spot', '5_youban': 'oil_spot', '6_siban': 'silk_spot',
            '7_yiwu': 'inclusion', '8_yahen': 'rolled_pit', '9_zhehen': 'waist_folding', '10_yaozhe': 'crease'}

0. puching_hole
1. welding_line 
2. crescent_gap 
3. water_spot 
4. oil_spot 
5. Silk spot  
6. Inclusion 
7. rolled_pit
8. waist_folding 
9. Crease
'''

# xml 파일 여러개를 json 파일 하나로 만들기
def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_detection\images'
    json_path = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_detection\anno\annotation.json'

    CLASS_NAME = {'crease': 0, 'crescent_gap': 1, 'inclusion': 2, 'oil_spot': 3, 'punching_hole': 4,
                  'rolled_pit': 5, 'silk_spot': 6, 'waist_folding': 7, 'water_spot': 8, 'welding_line': 9}

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    for filename in tqdm(json_data.keys()):
        image_path = os.path.join(data_root, filename)
        image = cv2.imread(image_path)
        json_image = json_data[filename]
        width = json_image['width']
        height = json_image['height']

        annos = json_image['anno']
        for anno in annos:
            label = anno['label']
            bbox = anno['bbox']

            label_class = CLASS_NAME[label]
            xmin, ymin, xmax, ymax = bbox
            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 255, 0), 1)


        image = cv2.resize(image, (width//2, height//2))
        cv2.imshow('visual', image)
        if cv2.waitKey(0) & 0xff == ord('q'):
            exit()


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