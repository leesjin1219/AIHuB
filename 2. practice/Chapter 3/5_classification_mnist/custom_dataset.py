from torch.utils.data import Dataset
import torchvision.transforms as transforms
from PIL import Image
import os

CLASS_NAME = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
class CustomDataset(Dataset):
    def __init__(self, data_root):
        self.image_paths = get_img_paths(data_root)
        self.labels = []
        for image_path in self.image_paths:
            label = image_path.split('\\')[-2]
            self.labels.append(CLASS_NAME[label])

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(image_path)
        image = transforms.ToTensor()(image)
        #  tensors, numpy arrays

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
