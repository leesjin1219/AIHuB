import cv2
import imgaug.augmenters as iaa
def main():

    # test할 이미지 선택(경로)
    image_path = 'C:\\Users\\user\\Pictures\\cat.jpg'
    image = cv2.imread(image_path)

    seq = iaa.Sequential(
        [
            iaa.Fliplr(0.5), # 좌우 반전
            iaa.Affine(
                rotate=(-90, 90) # 회전
            )
        ]
    )

    image_aug = seq(images=[image])[0]

    cv2.imshow('original', image)
    cv2.imshow('aug', image_aug)

    cv2.waitKey(0)

if __name__ == '__main__':
    main()