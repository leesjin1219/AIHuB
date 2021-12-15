import cv2
import numpy as np
import os


def main():
    image_root = 'C:\\Users\\user\\Desktop\\AIHub data zip\\5. steel_damaged\\image'
    mask_root = 'C:\\Users\\user\\Desktop\\AIHub data\\5. steel_damaged\\\masks'

    image_paths = get_img_paths(image_root)
    for image_path in image_paths:
        filename = os.path.basename(image_path)
        mask_path = os.path.join(mask_root, filename)

        image = cv2.imread(mask_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        mask_image = np.ones((256, 256), dtype=np.uint8) # * 250

        print(type(mask_image))
        print(type(image))

        print(mask_image.shape)
        print(image.shape)

        print(cv2.countNonZero(image))

        # new = cv2.bitwise_and(mask_image, image)
        # print(cv2.countNonZero(image))
        new = mask_image * image

        ori_image = cv2.imread(image_path)
        print(type(ori_image))
        print(ori_image.shape)
        ori_image = cv2.bitwise_and(ori_image, ori_image, mask=new)

        cv2.imshow('visual', ori_image)
        # cv2.imshow('mask', mask_image)
        cv2.imshow('new', new)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def get_img_paths(root_path):
    img_paths = []
    for (path, dir, files) in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng']
            if ext in formats:
                img_path = os.path.join(path, file)
                img_paths.append(img_path)
    return img_paths

if __name__ == '__main__':
    main()