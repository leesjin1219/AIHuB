from torch.utils.data import Dataset
import torchvision.transforms as transforms
import imgaug.augmenters as iaa
from PIL import Image
import cv2
import os

CLASS_NAME = {'acceptance': 0, 'defective': 1}
class CustomDataset(Dataset):
    def __init__(self, data_root, status='train'):
        self.status = status
        self.image_paths = get_img_paths(data_root)
        self.labels = []
        for image_path in self.image_paths:
            label = image_path.split('\\')[-2]
            self.labels.append(CLASS_NAME[label])
        self.seq = iaa.Sequential([
            iaa.Fliplr(0.5), # 좌우 반전
            ]
        )

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        image = cv2.imread(image_path)
        if self.status == 'train':
            image = self.seq(images=[image])[0]

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = transforms.ToTensor()(image)

        return {'label': label, 'image': image}

    def __len__(self):
        return len(self.image_paths)

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
