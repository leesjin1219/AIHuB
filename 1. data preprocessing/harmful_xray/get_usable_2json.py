import cv2
import numpy as np
import os
from xml.etree.ElementTree import parse, Element, dump, ElementTree
import json
from tqdm import tqdm

def main():
    # json_path = 'C:\\Users\\user\\Desktop\\AIHub data zip\\6. airport_xray\\anno\\annotation.json'
    #
    # image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\6. airport_xray\\Smith'
    # save_root = 'C:\\Users\\user\\Desktop\\AIHub data zip\\6. airport_xray\\image'
    # os.makedirs(save_root, exist_ok=True)
    #
    # filename_list = {}
    # img_paths = get_img_paths(image_root)
    # for img_path in img_paths:
    #     filename = os.path.basename(img_path)
    #     filename_list[filename] = img_path
    #
    # with open(json_path, 'r') as j:
    #     json_data = json.load(j)
    # print(len(json_data.keys()))
    # for filename in json_data.keys():
    #     image_image = json_data[filename]
    #     annos = image_image['anno']
    #     is_mixed = False
    #     labels = []
    #     for anno in annos:
    #         label = anno['label']
    #         labels.append(label)
    #     labels = set(labels)
    #     if len(labels) > 1:
    #         print(filename_list[filename])
    # exit()


    xml_roots = ['C:\\Users\\user\\Desktop\\AIHub data\\6. airport_xray\\Annotation\\Train\\Pascal\\Smith',
                 'C:\\Users\\user\\Desktop\\AIHub data\\6. airport_xray\\Annotation\\Label\\Pascal\\Smith']

    image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\6. airport_xray\\Smith'
    save_root_anno = 'C:\\Users\\user\\Desktop\\AIHub data zip\\6. airport_xray\\anno\\annotation.json'

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

    filename_list = {}
    filename_ids = []
    img_paths = get_img_paths(image_root)
    for img_path in img_paths:
        filename = os.path.basename(img_path)
        filename_list[filename] = img_path
        filename_ids.append(filename[:-4])

    for xml_root in xml_roots:
        xml_paths = get_xml_paths(xml_root)
        for xml_path in xml_paths:
            filename_xml = os.path.basename(xml_path)
            xml_id = filename_xml[:-4]
            if xml_id not in filename_ids:
                continue

            root = parse(xml_path).getroot()
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

            is_usuable_image = False
            objs = root.findall('object')
            for obj in objs:
                name = obj.find('name').text
                bndbox = obj.find('bndbox')
                xmin = bndbox.find('xmin').text
                ymin = bndbox.find('ymin').text
                xmax = bndbox.find('xmax').text
                ymax = bndbox.find('ymax').text

                if name not in ['Knife', 'Gun']:
                    continue
                else:
                    is_usuable_image = True

                json_obj = {
                    'label': name,
                    'bbox': [int(xmin), int(ymin), int(xmax), int(ymax)]
                }
                json_image['anno'].append(json_obj)
            json_data[filename] = json_image

    with open(save_root_anno, 'w') as j:
        json.dump(json_data, j, indent='\t')






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