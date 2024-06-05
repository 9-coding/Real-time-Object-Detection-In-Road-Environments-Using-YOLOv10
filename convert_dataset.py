import os
import shutil
import json
import time

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
annotation_path = raw_path + '/Validation/Annotations/1.TOA' # 원본 파일 내 json 파일 경로


# image와 annotation의 이름이 매칭이 안 되는 파일 제거.
def drop_files(annot_path, image_path):
    print("\nChecking files ...")
    n = 0
    file_list = os.listdir(annot_path)
    for annot_file in file_list:
        img_file = annot_file[:-10] + '.png'
        img_path = image_path + '/' + img_file
        if not os.path.exists(img_path):
            n += 1
    print(f"Drop {n} mismatched files")

# 임시 데이터셋, 최종 데이터셋 폴더 생성
def make_dirs():
    temp = "temp_dataset"
    dataset = "dataset"
    if not os.path.exists("temp_dataset"):
        os.makedirs(os.path.join(temp, "temp_images"))
        os.makedirs(os.path.join(temp, "temp_annotations"))
        os.makedirs(os.path.join(temp, "Images"))
        os.makedirs(os.path.join(temp, "Annotations"))

    if not os.path.exists(dataset):
        os.mkdir(dataset)

def set_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding

def get_label_num(labels):
    n_labels = [0] * 10
    for i in range(len(class_list)):
        n_labels[i] = len(labels[i])
    return n_labels


# --------------------------------------------------------------------------


# 데이터셋 경로를 쉽게 변경.
# 또한 옮기는 과정에서 중복 제거
def export_files(folder_list):
    print("\nExport Dataset:")
    print(f'raw_dataset -> temp_dataset')
    for folder in folder_list:
        print(folder+" ... " )
        img_path = os.path.join(image_path, folder)
        annot_path = os.path.join(annotation_path, folder)
        img_list = os.listdir(img_path)
        annot_list = os.listdir(annot_path)
        count = 0
        for file in img_list:
            percent = round(count / len(img_list) * 100, 2)
            print(f"\r {percent}%: {file}", end="")
            count += 1
            try:
                shutil.copy(os.path.join(img_path, file), "temp_dataset/temp_images")
            except Exception as e:
                continue
        for file in annot_list:
            try:
                shutil.copy(os.path.join(annot_path, file), "temp_dataset/temp_annotations")
            except Exception as e:
                continue
        print()


# 각 이미지의 라벨을 추출하는 함수
def num_labels(file, file_path, labels, file_names):
    # 인코딩 감지
    encoding = set_encoding(file_path)

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
                labels[id - 1].append(file)
                file_names[id - 1].append(file)
                #categories[id - 1].append(file)

    except UnicodeDecodeError as e:
        pass #print(f"Error decoding file {file_path}: {e}")
    except json.JSONDecodeError as e:
        pass #print(f"Error parsing JSON file {file_path}: {e}")

    return labels, file_names

# 원본 데이터셋의 정보 출력 및 저장
def label_info(annot_path):
    print("\nReading files ...")

    n_files = 0
    labels = [[] for _ in range(10)]
    file_names = [[] for _ in range(10)]
    file_list = os.listdir(annot_path)
    count = 0

    for file in file_list:
        percent = round(count / len(file_list)* 100, 2)
        print(f"\r {percent}%: {file}", end="")
        n_files += 1
        file_path = os.path.join(annot_path, file)
        labels, file_names = num_labels(file, file_path, labels, file_names)
        count += 1

    # 정보 출력
    print(f"\n\nnumber of files in dataset: {n_files}")
    n_labels = get_label_num(labels)
    for label, num in zip(class_list, n_labels):
        print(label + ': '+str(num))
    return labels, file_names

def get_class_num(folder_path, label):
    file_list = os.listdir(folder_path)
    n_labels = 0
    for file in file_list:
        file_path = os.path.join(folder_path, file)
        encoding = set_encoding(file_path)
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
                category_ids = []

                # 파일 내의 모든 annotations 검사
                for annotation in data['annotations']:
                    category_ids.append(annotation['category_id'])

                # 고유한 category_ids 추출
                unique_category_ids = np.unique(category_ids)
                if label in unique_category_ids:
                    n_labels += 1

        except UnicodeDecodeError as e:
            print(f"Error decoding file {file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {file_path}: {e}")
    return n_labels


def balance_dataset():
    print("\nSet balance each label:")
    file_list = os.listdir("temp_dataset/temp_annotations")
    max_size = 10000

    for i in range(10):  # i는 class.
        print(file_list[i])
        print(class_list[i])
        iter = 0
        print("이미 데이터셋에 해당 클래스가 10000개인지 확인")
        num = get_class_num("temp_dataset/Annotations", i + 1)
        if num < 10000:
            print(class_list[i]+f": 10000개 이하. ({num}개)")
            for file in file_list:  # 전체에서 클래스가 i인 파일을 찾아서 옮김.
                if iter >= max_size:
                    break  # max_size에 도달하면 루프 종료
                index = file_list.index(file)

                file_path = "temp_dataset/temp_annotations/" + file
                if not os.path.exists(file_path):
                    continue
                img_file = file[:-10] + '.png'
                encoding = set_encoding(file_path)

                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        data = json.load(f)
                        category_ids = []

                        for annotation in data['annotations']:
                            category_ids.append(annotation['category_id'])

                        unique_category_ids = np.unique(category_ids)
                        for id in unique_category_ids:
                            if id == i + 1:
                                try:
                                    shutil.copy("temp_dataset/temp_images/" + img_file,
                                                "temp_dataset/Images/" + img_file)
                                except Exception as e:
                                    continue#print(e)
                                try:
                                    shutil.copy("temp_dataset/temp_annotations/" + file,
                                                "temp_dataset/Annotations/" + file)
                                except Exception as e:
                                    continue#print(e)
                                iter += 1  # 파일을 이동한 후 iter 증가
                                if iter >= max_size:
                                    break  # max_size에 도달하면 내부 루프도 종료
                except Exception as e:
                    print(e)
                    continue
        else:
            print(class_list[i]+": 이미 10000개 존재")
            continue

make_dirs() # 결과 폴더 만들기
#export_files(folder_list) # 원본 데이터셋에서 파일만 추출
#drop_files("temp_dataset/temp_annotations", "temp_dataset/temp_images") # 이미지와 라벨 이름이 일치하지 않는 파일 제거
#labels, file_names= label_info("temp_dataset/temp_annotations") # 라벨 정보 추출

balance_dataset() # 라벨 균형 맞추기
print("\n----- After balancing dataset -----")
labels, file_names=label_info("temp_dataset/Annotations")

