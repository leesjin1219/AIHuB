import random
import shutil
import os
from tqdm import tqdm

random.seed(333)

def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_augmented'
    save_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_split'
    data_types = ['train', 'valid', 'test']
    labels = os.listdir(data_root)

    for data_type in data_types:
        for label in labels:
            path = os.path.join(save_root, data_type, label)
            os.makedirs(path, exist_ok=True)

    for label in labels:
        image_root = os.path.join(data_root, label)
        image_paths = get_img_paths(image_root)
        random.shuffle(image_paths)

        train_idx = int(0.7 * len(image_paths))
        valid_idx = train_idx + int(0.2 * len(image_paths))
        train, valid, test = image_paths[:train_idx], image_paths[train_idx:valid_idx], image_paths[valid_idx:]

        data_list = [train] + [valid] + [test]
        for type_idx, paths in enumerate(data_list):
            data_type = data_types[type_idx]
            for image_path in tqdm(paths, desc=f'{data_type}:'):
                filename = os.path.basename(image_path)
                save_path = os.path.join(save_root, data_type, label, filename)
                shutil.copy2(image_path, save_path)

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

if __name__ == '__main__':
    main()