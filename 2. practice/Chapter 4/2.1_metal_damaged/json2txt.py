import json
import os
from tqdm import tqdm

def main():
    json_path = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_detection\anno\annotation.json'
    save_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_detection\labels'
    os.makedirs(save_root, exist_ok=True)

    CLASS_NAME = {'crease': 0, 'crescent_gap': 1, 'inclusion': 2, 'oil_spot': 3, 'punching_hole': 4,
                  'rolled_pit': 5, 'silk_spot': 6, 'waist_folding': 7, 'water_spot': 8, 'welding_line': 9}

    with open(json_path, 'r') as j:
        json_data = json.load(j)

    # json_image: {'filename': 'H_8211.91-0000_01_001.png', 'width': 1680, 'height': 1050, 'anno': [{'label': 'Knife', 'bbox': [245, 237, 603, 564]}, {'label': 'Knife', 'bbox': [1162, 153, 1473, 509]}]}
    for filename in tqdm(json_data.keys()):
        json_image = json_data[filename]

        filename_save = os.path.splitext(filename)[0] + '.txt'
        save_path = os.path.join(save_root, filename_save)
        f = open(save_path, 'w')

        width = json_image['width']
        height = json_image['height']
        annos = json_image['anno']
        for anno in annos:
            label = anno['label']
            bbox = anno['bbox']

            label_class = CLASS_NAME[label]
            x_center = (bbox[0] + bbox[2]) / 2
            y_center = (bbox[1] + bbox[3]) / 2
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            write = f'{label_class} {x_center/width} {y_center/height} {w/width} {h/height}\n'
            f.write(write)

        f.close()

if __name__ == '__main__':
    main()