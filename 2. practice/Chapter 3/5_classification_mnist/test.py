import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import torchvision.transforms as transforms
from PIL import Image
import cv2

class ConvNet(nn.Module):
    def __init__(self):  # layer 정의
        super(ConvNet, self).__init__()

        # input size = 28x28
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)  # input channel = 1, filter = 10, kernel size = 5, zero padding = 0, stribe = 1
        # ((W-K+2P)/S)+1 공식으로 인해 ((28-5+0)/1)+1=24 -> 24x24로 변환
        # maxpooling하면 12x12

        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)  # input channel = 1, filter = 10, kernel size = 5, zero padding = 0, stribe = 1
        # ((12-5+0)/1)+1=8 -> 8x8로 변환
        # maxpooling하면 4x4

        self.drop2D = nn.Dropout2d(p=0.25, inplace=False)  # 랜덤하게 뉴런을 종료해서 학습을 방해해 학습이 학습용 데이터에 치우치는 현상을 막기 위해 사용
        self.mp = nn.MaxPool2d(2)  # 오버피팅을 방지하고, 연산에 들어가는 자원을 줄이기 위해 maxpooling
        self.fc1 = nn.Linear(320, 100)  # 4x4x20 vector로 flat한 것을 100개의 출력으로 변경
        self.fc2 = nn.Linear(100, 10)  # 100개의 출력을 10개의 출력으로 변경

    def forward(self, x):
        x = F.relu(self.mp(self.conv1(x)))  # convolution layer 1번에 relu를 씌우고 maxpool, 결과는 12x12x10
        x = F.relu(self.mp(self.conv2(x)))  # convolution layer 2번에 relu를 씌우고 maxpool, 결과는 4x4x20
        x = self.drop2D(x)
        x = x.view(x.size(0), -1)  # flat
        x = self.fc1(x)  # fc1 레이어에 삽입
        x = self.fc2(x)  # fc2 레이어에 삽입
        return F.log_softmax(x)  # fully-connected layer에 넣고 log softmax 적용

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_path = './weights/9.pth'
    model = ConvNet()
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()

    test_root = r'C:\Users\user\Desktop\AIHub data zip\7. mnist\test'
    test_paths = get_img_paths(test_root)
    with torch.no_grad():
        for test_path in test_paths:
            image = Image.open(test_path)
            image = transforms.ToTensor()(image).unsqueeze(0).to(device)
            outputs = model(image)
            _, predictions = torch.max(outputs.data, 1)
            print(predictions.item())
            image_cv2 = cv2.imread(test_path)
            image_cv2 = cv2.resize(image_cv2, (200, 200))
            cv2.imshow('visual', image_cv2)
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