import os
import cv2

def main():

    image_root = 'C:\\Users\\user\\Desktop\\AIHub data\\1. casting_defective'

    # step 1: 데이터 폴더 내 파일 확인하기
    files = os.listdir(image_root)
    # print('파일 개수: ', len(files))
    # for filename in os.listdir(image_root):
    #     print(filename)

    # step 2: 파일 이름을 읽고, 양품과 불량품을 구분하여 폴더에 정리하기
    acc_root = 'C:\\Users\\user\\Desktop\\AIHub data\\1. casting_defective\\acceptance'  # get path
    def_root = 'C:\\Users\\user\\Desktop\\AIHub data\\1. casting_defective\\defective'

    os.makedirs(acc_root, exist_ok=True)
    os.makedirs(def_root, exist_ok=True)

    for filename in files:
        if '.' not in filename: # 파일이름이 아닌 경우 제외
            continue
        if 'ok' in filename:
            save_path = os.path.join(acc_root, filename)
        elif 'def' in filename:
            save_path = os.path.join(def_root, filename)

        image_path = os.path.join(image_root, filename)
        image = cv2.imread(image_path)

        cv2.imwrite(save_path, image)





if __name__ == '__main__':
    main()