import cv2
import numpy as np
import os
from xml.etree.ElementTree import parse, Element, dump, ElementTree
from tqdm import tqdm

def main():
    xml_root = 'C:\\Users\\user\\Desktop\\AIHub data\\4. automotive_engine_damaged\\labelimg\\Annotations'
    image_root = 'C:\\Users\\user\\Desktop\\AIHub data zip\\4. automotive_engine_damaged\\image'
    save_root_xml = 'C:\\Users\\user\\Desktop\\AIHub data zip\\4. automotive_engine_damaged\\anno\\annotation.xml'

    xml_data = Element('annotation')

    xml_paths = get_xml_paths(xml_root)
    for xml_path in xml_paths:
        xml_image = Element('image')

        root = parse(xml_path).getroot()
        filename = root.find('filename').text

        size = root.find('size')
        width = size.find('width').text
        height = size.find('height').text

        xml_image.attrib['filename'] = filename
        xml_image.attrib['width'] = width
        xml_image.attrib['height'] = height

        objs = root.findall('object')
        for obj in objs:
            name = obj.find('name').text
            if name == 'bumpinjury':
                xml_bbox = Element('bbox')

                bndbox = obj.find('bndbox')
                xmin = bndbox.find('xmin').text
                ymin = bndbox.find('ymin').text
                xmax = bndbox.find('xmax').text
                ymax = bndbox.find('ymax').text

                xml_bbox.attrib['label'] = 'bump_injury'
                xml_bbox.attrib['xmin'] = xmin
                xml_bbox.attrib['ymin'] = ymin
                xml_bbox.attrib['xmax'] = xmax
                xml_bbox.attrib['ymax'] = ymax

                xml_image.append(xml_bbox)
        xml_data.append(xml_image)
        indent(xml_data)
        # dump(xml_data)
    ElementTree(xml_data).write(save_root_xml)



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