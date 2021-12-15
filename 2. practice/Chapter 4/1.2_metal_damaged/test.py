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
    weight_path = './weights/best.pth'

    # model 지정
    model = models.__dict__['resnet18'](pretrained=False, num_classes=10)
    model = model.to(device)
    checkpoint = torch.load(weight_path)
    model.load_state_dict(checkpoint)
    model.eval()

    # batch size 지정
    batch_size = 16

    # 환경에 맞추어 작성된(custom) Dataset 사용
    test_root = r'C:\Users\user\Desktop\AIHub data zip\2. metal_damaged_classification_cropped_split\test'
    test_dataset = CustomDataset(test_root, 'test')
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)

    # 검증-Test
    with torch.no_grad():

        CLASS_NAME = ['crease', 'crescent_gap', 'inclusion', 'oil_spot', 'punching_hole',
                      'rolled_pit', 'silk_spot', 'waist_folding', 'water_spot', 'welding_line']
        truth = {'crease': 0, 'crescent_gap': 0, 'inclusion': 0, 'oil_spot': 0, 'punching_hole': 0,
             'rolled_pit': 0, 'silk_spot': 0, 'waist_folding': 0, 'water_spot': 0, 'welding_line': 0}
        correct = {'crease': 0, 'crescent_gap': 0, 'inclusion': 0, 'oil_spot': 0, 'punching_hole': 0,
             'rolled_pit': 0, 'silk_spot': 0, 'waist_folding': 0, 'water_spot': 0, 'welding_line': 0}


        for items in tqdm(test_loader):
            images = items['image'].to(device)
            labels = items['label'].to(device)

            outputs = model(images)
            _, predictions = torch.max(outputs.data, 1)

            for idx, image in enumerate(images):
                print(CLASS_NAME[predictions[idx].item()])
                image_cv2 = image.cpu().numpy().transpose(1,2,0) # pil -> cv2
                cv2.imshow('test visual', image_cv2)
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    exit()

            for idx, label in enumerate(labels):
                label = label.cpu().item()
                prediction = predictions[idx].cpu().item()

                truth[CLASS_NAME[label]] += 1
                if label == prediction:
                    correct[CLASS_NAME[label]] += 1

    for cls in CLASS_NAME:
        sensitivity = correct[cls] / truth[cls]
        specificity = (sum(correct.values()) - correct[cls]) / (sum(truth.values()) - truth[cls])
        print(f'{cls}: Sensitivity-{sensitivity}, Specificity-{specificity}')
    accuracy = sum(correct.values()) / sum(truth.values())
    print(f'Accuracy: {accuracy}')

if __name__ == '__main__':
    main()