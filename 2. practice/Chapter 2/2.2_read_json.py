import json
import os
import cv2

def main():

    data_root = r'C:\Users\user\Desktop\AIHub data zip\8. read_anno\read_json'
    json_paths = get_json_paths(data_root)

    for json_path in json_paths:
        with open(json_path, 'r') as j:
            json_data = json.load(j)

        # print(json_data.keys())
        category_list = json_data['categories']
        image_list = json_data['images']
        anno_list = json_data['annotations']

        for image_json in image_list:
            filename = image_json['file_name']
            image_id = image_json['id']
            image_path = os.path.join(data_root, 'image', filename)
            image = cv2.imread(image_path)

            for anno_json in anno_list:
                if image_id == anno_json['image_id']:
                    bbox = anno_json['bbox']
                    x, y, w, h = list(map(int, bbox))
                    image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)

                    # category_id = anno_json['category_id']
                    # category_json = category_list[category_id]
                    # category_name = category_json['name']
                    # image = cv2.putText(image, category_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('visual', image)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

def get_json_paths(root_path):
    file_paths = []
    for (path, dir, files) in os.walk(root_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            formats = ['.json']
            if ext in formats:
                file_path = os.path.join(path, file)
                file_paths.append(file_path)
    return file_paths


if __name__ == '__main__':
    main()