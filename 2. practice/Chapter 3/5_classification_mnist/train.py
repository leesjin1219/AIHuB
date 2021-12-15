import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from custom_dataset import CustomDataset
import os
from tqdm import tqdm

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
    # 컴퓨터 환경 설정: cuda를 사용할 수 있으면 cuda, 그렇지 않으면 cpu
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # 저장 경로 설정
    save_root = './weights'
    os.makedirs(save_root, exist_ok=True)

    # model 지정
    model = ConvNet().to(device)  # CNN instance 생성
    # import torchvision.models as models
    # model = models.__dict__['resnet18'](pretrained=False, num_classes=10)
    # model = model.to(device)

    # loss function, optimizer 지정하기
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # epoch, batch size 지정하기
    epoch = 10
    batch_size = 100
    
    # 환경에 맞추어 작성된(custom) Dataset 사용하기
    train_root = r'C:\Users\user\Desktop\AIHub data zip\7. mnist\train'
    train_dataset = CustomDataset(train_root)
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    # 학습-Training
    for epoch in range(epoch):
        for items in tqdm(train_loader, desc=f'{epoch:}'):
            images = items['image'].to(device)
            labels = items['label'].to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = loss_function(outputs, labels)

            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), f'{save_root}/{epoch}.pth')

if __name__ == '__main__':
    main()