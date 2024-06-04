import os
import shutil
import json
import numpy as np
import chardet

raw_path = 'raw_dataset' # 원본 데이터셋 경로
folder_list = ['1.Frontback_N01', '1.Frontback_N02', '1.Frontback_N03',
               '2.Highway_N01',
               '3.Industrialroads_N01', '3.Industrialroads_N02', '3.Industrialroads_N03',
               '4.Kidzone_N01', '4.Kidzone_N02',
               '5.Mainroad_N01', '5.Mainroad_N02'
               ] # 원본 파일 내 폴더 목록
class_list = ['Animals(Dolls)', 'Person', 'Garbage bag & sacks', 'Construction signs & Parking prohibited board',
              'Traffic cone', 'Box', 'Stones on road', 'Pothole on road', 'Filled pothole', 'Manhole']
max_size = 10000 # 각 label 별 최대 크기

image_path = raw_path + '/Validation/Images/1.TOA' # 원본 파일 내 이미지 파일 경로
annot_path = raw_path + '/Validation/Annotations/1.TOA' # 원본 파일 내 json 파일 경로

def label_info():
    labels = [0] * 10
    n_files = 0
    for folder in folder_list:
        print(folder)
        file_list = os.listdir(os.path.join(annot_path, folder))

        for file in file_list:
            n_files += 1
            file_path = os.path.join(annot_path, folder, file)

            # 인코딩 감지
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            # 파일이 비어있는지 확인
            if not raw_data:
                print(f"File is empty: {file_path}")
                continue

            # 파일을 감지된 인코딩으로 읽기
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    data = json.load(f)
                    category_ids = []

                    # 파일 내의 모든 annotations 검사
                    for annotation in data['annotations']:
                        category_ids.append(annotation['category_id'])

                    # 고유한 category_ids 추출
                    unique_category_ids = np.unique(category_ids)
                    for id in unique_category_ids:
                        labels[id - 1] += 1

            except UnicodeDecodeError as e:
                print(f"Error decoding file {file_path}: {e}")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file {file_path}: {e}")

    # 정보 출력
    print(f"number of files in dataset: {n_files}")
    for label, num in zip(class_list, labels):
        print(label + ': '+str(num))

def make_dirs():
    if not os.path.exists("temp_dataset"):
        os.makedirs("temp_dataset/images")
        os.makedirs("temp_dataset/annotations")

    if not os.path.exists("dataset"):
        os.mkdir("dataset")

label_info()
make_dirs()