import random
import shutil
import os

random.seed(333)

def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\4. automotive_engine_damaged'
    image_root = os.path.join(data_root, 'images')
    anno_root = os.path.join(data_root, 'labels')
    data_types = ['train', 'valid', 'test']
    for data_type in data_types:
        path = os.path.join(image_root, data_type)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(anno_root, data_type)
        os.makedirs(path, exist_ok=True)

    image_paths = get_img_paths(image_root)
    random.shuffle(image_paths)
    train_idx = int(0.7 * len(image_paths))
    valid_idx = train_idx + int(0.2 * len(image_paths))
    train, valid, test = image_paths[:train_idx], image_paths[train_idx:valid_idx], image_paths[valid_idx:]
    data_list = [train] + [valid] + [test]

    for type_idx, paths in enumerate(data_list):
        data_type = data_types[type_idx]
        for image_path in paths:
            filename = os.path.basename(image_path)
            txtname = filename[:-4]+'.txt'
            txt_path = os.path.join(anno_root, txtname)

            save_path_image = os.path.join(image_root, data_type, filename)
            save_path_txt = os.path.join(anno_root, data_type, txtname)
            shutil.move(image_path, save_path_image)
            shutil.move(txt_path, save_path_txt)

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