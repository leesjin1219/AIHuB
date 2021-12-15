import os
from xml.etree.ElementTree import parse

def main():
    xml_path = r'C:\Users\user\Desktop\AIHub data zip\4. automotive_engine_damaged\anno\annotation.xml'
    save_root = r'C:\Users\user\Desktop\AIHub data zip\4. automotive_engine_damaged\labels'
    os.makedirs(save_root, exist_ok=True)

    CLASS_NAME = {'bump_injury': 0}
    root = parse(xml_path).getroot()

    for xml_image in root.findall('image'):
        filename = xml_image.attrib['filename']
        filename_save = os.path.splitext(filename)[0] + '.txt'
        save_path = os.path.join(save_root, filename_save)
        f = open(save_path, 'w')

        width = int(xml_image.attrib['width'])
        height = int(xml_image.attrib['height'])
        for bbox in xml_image.findall('bbox'):
            label = bbox.attrib['label']
            xmin = int(bbox.attrib['xmin'])
            ymin = int(bbox.attrib['ymin'])
            xmax = int(bbox.attrib['xmax'])
            ymax = int(bbox.attrib['ymax'])

            label_class = CLASS_NAME[label]
            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2
            w = xmax - xmin
            h = ymax - ymin

            write = f'{label_class} {x_center/width} {y_center/height} {w/width} {h/height}\n'
            f.write(write)

        f.close()

if __name__ == '__main__':
    main()