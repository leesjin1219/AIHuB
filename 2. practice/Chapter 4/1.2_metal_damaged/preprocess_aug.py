import random
import os
import imgaug.augmenters as iaa
import cv2
import shutil
from tqdm import tqdm

random.seed(333)

def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped'
    save_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_augmented'
    seq = iaa.Sequential([
        iaa.Fliplr(0.5), # 좌우 반전
        iaa.Flipud(0.5), # 상하 반전
        iaa.Affine(
            rotate=(-90, 90) # 회전
        )])
    labels = os.listdir(data_root)

    count_goal = 900
    for label in labels:
        save_path_dir = os.path.join(save_root, label)
        os.makedirs(save_path_dir, exist_ok=True)

        label_root = os.path.join(data_root, label)
        image_paths = get_img_paths(label_root)
        for image_path in image_paths: # 이미지 원본 옮기기
            save_path = os.path.join(save_path_dir, os.path.basename(image_path))
            shutil.move(image_path, save_path)

        count_now = len(os.listdir(label_root))
        for i in tqdm(range(count_now, count_goal), desc=f"{label}:"):
            image_path = random.choice(image_paths)
            image = cv2.imread(image_path)
            image = seq(images=[image])[0]

            filename = os.path.basename(image_path)
            filename_save = os.path.splitext(filename)[0] + f'_{i}.png'
            save_path = os.path.join(save_path_dir, filename_save)
            cv2.imwrite(save_path, image)

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