from torch.utils.data import Dataset
import torchvision.transforms as transforms
from PIL import Image
import cv2
import os

CLASS_NAME = {'crease': 0, 'crescent_gap': 1, 'inclusion': 2, 'oil_spot': 3, 'punching_hole': 4,
             'rolled_pit': 5, 'silk_spot': 6, 'waist_folding': 7, 'water_spot': 8, 'welding_line': 9}
class CustomDataset(Dataset):
    def __init__(self, data_root, status='train'):
        self.status = status
        self.image_paths = get_img_paths(data_root)
        self.labels = []
        for image_path in self.image_paths:
            label = image_path.split('\\')[-2]
            self.labels.append(CLASS_NAME[label])

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        image = cv2.imread(image_path)
        image = image_padding(image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = transforms.ToTensor()(image)

        return {'label': label, 'image': image}

    def __len__(self):
        return len(self.image_paths)

def image_padding(image):
    width, height = 224, 224
    h, w, _ = image.shape

    if h > w:
        h_resize, w_resize = height, int(w / h * height)
    else: # h < w
        h_resize, w_resize = int(h / w * width), width
    image = cv2.resize(image, (w_resize, h_resize))

    top = int((height - h_resize) / 2)
    bottom = (height - h_resize) - top
    left = int((width - w_resize) / 2)
    right = (width - w_resize) - left
    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return image


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
