import torch
import cv2
import os

def main():
    test_root = '/home/bong04/data/airport_xray/images/test'

    image_paths = get_paths(test_root)
    for image_path in image_paths:
        model = torch.hub.load('./', 'custom', path='runs/train/exp3/weights/best.pt', source='local')
        model.conf = 0.7  # NMS confidence threshold

        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ori_img = img.copy()
        img = [img]  # batch of images

        results = model(img, size=640)
        rrs = results.xyxy[0].cpu().numpy()
        for rr in rrs:
            x1, y1, x2, y2, conf, cls = rr
            ori_img =cv2.rectangle(ori_img, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 1)

        h, w, _ = ori_img.shape
        ori_img = cv2.resize(ori_img, (w//2, h//2))
        cv2.imshow('1', ori_img)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()

def get_paths(root_path):
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

