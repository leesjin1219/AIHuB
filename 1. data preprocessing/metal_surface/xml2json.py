import os
import json
from xml.etree.ElementTree import parse
import cv2

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
    data_root = 'C:\\Users\\user\\Desktop\\AIHub data\\2. metal_damaged'
    save_root_anno = 'C:\\Users\\user\\Desktop\\AIHub data zip\\2. metal_damaged_detection\\anno'
    os.makedirs(save_root_anno, exist_ok=True)

    iron_dic = {'1_chongkong': 'punching_hole', '2_hanfeng': 'welding_line', '3_yueyawan': 'crescent_gap',
                '4_shuiban': 'water_spot', '5_youban': 'oil_spot', '6_siban': 'silk_spot',
                '7_yiwu': 'inclusion', '8_yahen': 'rolled_pit', '9_zhehen': 'waist_folding',
                '10_yaozhe': 'crease', '10_yaozhed': 'crease'}

    json_data = {}
    '''
    {
        'filename': {
            'filename': str,
            'width': int,
            'height': int,
            'anno': [
                {
                    'label': str,
                    'bbox': [xmin, ymin, xmax, ymax]
                }
            ]
        }
    }
    '''

    xml_paths = get_xml_paths(data_root)
    for xml_path in xml_paths:
        tree = parse(xml_path)
        root = tree.getroot()

        filename = root.find('filename').text

        size = root.find('size')
        width = size.find('width').text
        height = size.find('height').text

        json_image = {
            'filename': filename,
            'width': int(width),
            'height': int(height),
            'anno': []
        }

        objs = root.findall('object')
        for obj in objs:
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text

            if name == 'd':
                name = '1_chongkong'
            name = iron_dic[name]
            json_obj = {
                'label': name,
                'bbox': [int(xmin), int(ymin), int(xmax), int(ymax)]
            }
            json_image['anno'].append(json_obj)


        json_data[filename] = json_image

    json_path = os.path.join(save_root_anno, 'annotation.json')
    with open(json_path, 'w') as j:
        json.dump(json_data, j, indent='\t')





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