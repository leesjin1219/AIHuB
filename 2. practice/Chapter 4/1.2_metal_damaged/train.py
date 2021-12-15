import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
from torch.utils.data import DataLoader
from custom_dataset import CustomDataset
import os
from tqdm import tqdm


def main():
    # 컴퓨터 환경 설정
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # 저장 경로 설정
    save_root = './weights'
    os.makedirs(save_root, exist_ok=True)

    # model 지정
    model = models.__dict__['resnet18'](pretrained=False, num_classes=10)
    model = model.to(device)

    # loss function, optimizer 지정
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # epoch, batch size 지정
    epoch = 20
    batch_size = 16

    # 환경에 맞추어 작성된(custom) Dataset 사용
    train_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_split\train'
    train_dataset = CustomDataset(train_root)
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    valid_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_split\valid'
    valid_dataset = CustomDataset(valid_root, 'vaild')
    valid_loader = DataLoader(dataset=valid_dataset, batch_size=batch_size, shuffle=False)

    data_size = len(train_loader)
    best_score = 0
    # 학습-Training
    for epoch in range(epoch):
        model.train()
        losses = 0
        for items in tqdm(train_loader, desc=f'{epoch:}'):
            images = items['image'].to(device)
            labels = items['label'].to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()

            losses += loss

        # Validation
        model.eval()
        with torch.no_grad():
            correct = 0
            total = 0

            for items in valid_loader:
                images = items['image'].to(device)
                labels = items['label'].to(device)

                outputs = model(images)
                _, predictions = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predictions == labels).sum()  # .item()

        avg_loss = losses / data_size
        accuracy = correct / total
        print(f'epoch: {epoch} - Accuracy: {accuracy}, loss:{avg_loss}')

        if accuracy > best_score:
            best_score = accuracy
            torch.save(model.state_dict(), f'{save_root}/best.pth')
            print('best model saved')

        if epoch % 5 == 0:
            torch.save(model.state_dict(), f'{save_root}/{epoch}.pth')
            print('model saved')

if __name__ == '__main__':
    main()