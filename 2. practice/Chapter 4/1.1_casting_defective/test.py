import torch
import torchvision.models as models
from torch.utils.data import DataLoader
from custom_dataset import CustomDataset
import cv2
from tqdm import tqdm


def main():
    # 컴퓨터 환경 설정
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # 모델 weight path 지정
    weight_path = './weights/5.pth'

    # model 지정
    model = models.__dict__['resnet18'](pretrained=False, num_classes=10)
    model = model.to(device)
    checkpoint = torch.load(weight_path)
    model.load_state_dict(checkpoint)
    model.eval()

    # batch size 지정
    batch_size = 16

    # 환경에 맞추어 작성된(custom) Dataset 사용
    test_root = r'C:\Users\user\Desktop\AIHub data zip\1. casting_defective_labelled_split\test'
    test_dataset = CustomDataset(test_root, 'test')
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)

    # 검증-Test
    with torch.no_grad():
        CLASS_NAME = ['acceptance', 'defective']
        truth = {'acceptance': 0, 'defective': 0}
        correct = {'acceptance': 0, 'defective': 0}


        for items in tqdm(test_loader):
            images = items['image'].to(device)
            labels = items['label'].to(device)

            outputs = model(images)
            _, predictions = torch.max(outputs.data, 1)

            # for idx, image in enumerate(images):
            #     print(predictions[idx].item())
            #     image_cv2 = image.cpu().numpy().transpose(1,2,0) # pil -> cv2
            #     cv2.imshow('test visual', image_cv2)
            #     if cv2.waitKey(0) & 0xFF == ord('q'):
            #         cv2.destroyAllWindows()
            #         exit()

            for idx, label in enumerate(labels):
                label = label.cpu().item()
                prediction = predictions[idx].cpu().item()

                truth[CLASS_NAME[label]] += 1
                if label == prediction:
                    correct[CLASS_NAME[label]] += 1

    precision = correct['defective'] / (correct['defective'] + truth['acceptance']-correct['acceptance'])
    recall = correct['defective'] / truth['defective']
    specificity = correct['acceptance'] / truth['acceptance']
    accuracy = sum(correct.values()) / sum(truth.values())
    print(f'Precision: {precision}, Recall: {recall}')
    print(f'Sensitivity: {recall}, Specificity: {specificity}')
    print(f'Accuracy: {accuracy}')


if __name__ == '__main__':
    main()