from torch.utils.data import Dataset, DataLoader
import cv2
import os

CLASS_NAME = {'acceptance': 0, 'defective': 1}
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
        image = cv2.imread(image_path)
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

def main():
    data_root = r'C:\Users\user\Desktop\AIHub data zip\1. casting_defective_labelled_split\train'
    image_set = CustomDataset(data_root)
    image_loader = DataLoader(dataset=image_set, batch_size=16, shuffle=True)

    for items in image_loader:
        labels = items['label']
        images = items['image']
        for idx, image in enumerate(images):
            image = image.numpy()
            image = cv2.putText(image, str(labels[idx].numpy()), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('visual', image)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

if __name__ == '__main__':
    main()