import os
import shutil
import cv2

# xml 파일이 있는 이미지만 사용하기
def main():
    data_root = 'C:\\Users\\user\\Desktop\\AIHub data\\2. metal_damaged'
    save_root_img = 'C:\\Users\\user\\Desktop\\AIHub data zip\\2. metal_damaged_detection\\image'
    os.makedirs(save_root_img, exist_ok=True)

    img_paths = get_img_paths(data_root)
    xml_paths = get_xml_paths(data_root)

    xml_filenames = []
    for xml_path in xml_paths:
        filename = os.path.basename(xml_path)
        filename = filename.split('.')[0] + '.jpg'
        xml_filenames.append(filename)

    for img_path in img_paths:
        filename = os.path.basename(img_path)
        if filename in xml_filenames:
            save_path = os.path.join(save_root_img, filename)
            shutil.copy2(img_path, save_path)


    # filename = []
    # for directory in os.listdir(image_root):
    #     dir_path = os.path.join(image_root, directory)
    #     filename.extend(os.listdir(dir_path))
    # filename = set(filename)
    # print(len(filename))


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