import os
import shutil
import json
import numpy as np
import chardet

folder_list = ['1.Frontback_N01', '1.Frontback_N02', '1.Frontback_N03',
               '2.Highway_N01',
               '3.Industrialroads_N01', '3.Industrialroads_N02', '3.Industrialroads_N03',
               '4.Kidzone_N01', '4.Kidzone_N02',
               '5.Mainroad_N01', '5.Mainroad_N02'
               ] # 원본 파일 내 폴더 목록
class_list = ['Animals(Dolls)', 'Person', 'Garbage bag & sacks', 'Construction signs & Parking prohibited board',
              'Traffic cone', 'Box', 'Stones on road', 'Pothole on road', 'Filled pothole', 'Manhole']
max_size = 10000 # 각 label 별 최대 크기

raw_path = 'raw_dataset' # 원본 데이터셋 경로
image_path = raw_path + '/Validation/Images/1.TOA' # 원본 파일 내 이미지 파일 경로
annot_path = raw_path + '/Validation/Annotations/1.TOA' # 원본 파일 내 json 파일 경로


def get_label_num(labels):
    n_labels = [0] * 10
    for i in range(len(class_list)):
        n_labels[i] = len(labels[i])
    return n_labels

# 각 이미지의 라벨을 추출하는 함수
def num_labels(file, file_path, labels, file_names):
    # 인코딩 감지
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

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
                labels[id - 1].append(file_path)
                file_names[id - 1].append(file_path[41:-10])
                #categories[id - 1].append(file)

    except UnicodeDecodeError as e:
        print(f"Error decoding file {file_path}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file {file_path}: {e}")

    return labels, file_names

# 원본 데이터셋의 정보 출력 및 저장
def label_info(folder_list, annot_path):
    print("\nReading files ...")
    n_files = 0
    labels = [[] for _ in range(10)]
    file_names = [[] for _ in range(10)]

    for folder in folder_list:
        print(folder)
        file_list = os.listdir(os.path.join(annot_path, folder))

        for file in file_list:
            n_files += 1
            file_path = os.path.join(annot_path, folder, file)
            labels, file_names = num_labels(file, file_path, labels, file_names)

    # 정보 출력
    print(f"\nnumber of files in dataset: {n_files}")
    n_labels = get_label_num(labels)
    for label, num in zip(class_list, n_labels):
        print(label + ': '+str(num))
    return labels, file_names

# image와 annotation의 이름이 매칭이 안 되는 파일 제거.
def drop_files(folder_list, annot_path, image_path):
    print("\nChecking files ...")
    for folder in folder_list:
        file_list = os.listdir(os.path.join(annot_path, folder))
        for annot_file in file_list:
            file_path = annot_path+'/'+folder+'/'+annot_file
            img_file = annot_file[:-10] + '.png'
            img_path = image_path+'/'+folder+'/'+img_file
            if not os.path.exists(img_path):
                print("Does not exists: "+img_path)
            #print(file_path)



# 임시 데이터셋, 최종 데이터셋 폴더 생성
def make_dirs():
    temp = "temp_dataset"
    dataset = "dataset"
    if not os.path.exists("temp_dataset"):
        os.makedirs(os.path.join(temp, "images"))
        os.makedirs(os.path.join(temp, "annotations"))

    if not os.path.exists(dataset):
        os.mkdir(dataset)


def move_files(src_img, src_annot, dst, file):
    move_img = dst + '/images'
    move_annot = dst + '/annotations'
    img = file + '.png'
    annot = file + '_BBOX.json'

    try:
        # image 이동
        shutil.copy(src_img, os.path.join(move_img, img))
        # annotation 이동
        shutil.copy(src_annot, os.path.join(move_annot, annot))
    except Exception as e:
        print(e)
        return

def balance_dataset(src, dst, labels, file_names):
    print("\nExport Dataset:")
    print(f'{src} -> {dst}')
    # n_labels = [10520, 43433, 9144, 8076, 30534, 23962, 8189, 5000, 4284, 18752]
    n_labels = get_label_num(labels)
    image = [[] for _ in range(10)]
    p = 0
    for i in range(1):
        print(class_list[i])
        for j in range(n_labels[i]):
            if j < max_size:
                image[i].append(image_path + '/' + file_names[i][j] + '.png')
                move_files(image[i][j], labels[i][j], dst, file_names[i][j].split('/')[1])
            else:
                break


labels, file_names=label_info(folder_list, annot_path) # 라벨 정보 추출
drop_files(folder_list, annot_path, image_path)
make_dirs() # 결과 폴더 만들기
balance_dataset(raw_path, "temp_dataset", labels, file_names) # 라벨 균형 맞추기

print("\n----- After exporting dataset -----")
folder_list = ['annotations'] # image는 필요없음
labels=label_info(folder_list, "temp_dataset")