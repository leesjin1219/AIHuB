from xml.etree.ElementTree import parse
import os
import cv2

def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\8. read_anno\read_xml'
    img_paths = get_img_paths(data_root)

    for img_path in img_paths:
        filename = os.path.basename(img_path)
        filename_xml = os.path.splitext(filename)[0] + '.xml'
        xml_path = os.path.join(data_root, 'anno', filename_xml)

        image = cv2.imread(img_path)

        root = parse(xml_path).getroot()
        annos = root.findall('object')
        for anno in annos:
            label = anno.find('name').text
            bbox = anno.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)
            # image = cv2.putText(image, label, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('visual', image)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()

def get_img_paths(root_path):
    file_paths = []
    for (path, dir, files) in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng']
            if ext in formats:
                file_path = os.path.join(path, file)
                file_paths.append(file_path)
    return file_paths

if __name__ == '__main__':
    main()