import shutil
import os


def main():
    original_root = 'C:\\Users\\user\\Desktop\\AIHub data\\8. read_anno\\Chess Pieces.v24-416x416_aug.voc'
    save_root_xml = 'C:\\Users\\user\\Desktop\\AIHub data zip\\8. read_anno\\read_xml\\anno'
    save_root_img = 'C:\\Users\\user\\Desktop\\AIHub data zip\\8. read_anno\\read_xml\\image'

    xml_paths = get_xml_paths(original_root)
    img_paths = get_img_paths(original_root)

    for xml_path in xml_paths:
        filename = os.path.basename(xml_path)
        save_path = os.path.join(save_root_xml, filename)

        shutil.copy2(xml_path, save_path)

    for img_path in img_paths:
        filename = os.path.basename(img_path)
        save_path = os.path.join(save_root_img, filename)

        shutil.copy2(img_path, save_path)



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