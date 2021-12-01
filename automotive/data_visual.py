import cv2
import numpy as np
import os
from xml.etree.ElementTree import parse, Element, dump, ElementTree
from tqdm import tqdm

def main():
    xml_root = 'C:\\Users\\user\\Desktop\\AIHub data\\automotive_engine\\labelimg\\Annotations'
    image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\automotive_engine\\labelimg\\JPEGImages'

    image_paths = get_img_paths(image_root)
    filenames = []
    for image_path in image_paths:
        fileID = os.path.basename(image_path).split('.')[0]
        xml_path = os.path.join(xml_root, f'{fileID}.xml')
        image = cv2.imread(image_path)
        root = parse(xml_path).getroot()

        for bbox in root.findall('object'):
            coord = bbox.find('bndbox')

            coord.find('xmin')

            xmin = int(coord.find('xmin').text)
            ymin = int(coord.find('ymin').text)
            xmax = int(coord.find('xmax').text)
            ymax = int(coord.find('ymax').text)

            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 255), 1)

        cv2.imshow('visual', image)
        if cv2.waitKey(0) & 0xff == ord('q'):
            exit()





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