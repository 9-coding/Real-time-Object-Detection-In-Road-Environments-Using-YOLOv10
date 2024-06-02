import shutil
import os
import splitfolders


init_path = 'init_dataset'
data_path = 'temp_dataset'
image_path = init_path + '/images'
annotation_path = init_path + '/annotations'
folder_list = ['1.Frontback_W01', '2.Highway_M01', '3.Industrialroads_T01', '4.Kidzone_R02']


if not os.path.exists("temp_dataset"):
    os.makedirs("temp_dataset/images")
    os.makedirs("temp_dataset/annotations")

if not os.path.exists("dataset"):
    os.mkdir("dataset")

def move_files(src, dst, file):
    shutil.copy(os.path.join(src, file), os.path.join(dst, file))

# export files
for folder in folder_list:
    print(folder)
    image_folder = os.path.join(image_path, folder)
    annotation_folder = os.path.join(annotation_path, folder)

    if not os.path.exists(annotation_folder):
        print(f"Error: Annotation folder '{annotation_folder}' does not exist.")
        continue

    if not os.path.exists(image_folder):
        print(f"Error: Image folder '{image_folder}' does not exist.")
        continue

    file_list = os.listdir(annotation_folder)
    print(file_list[0:5])

    for file in file_list:
        move_files(annotation_folder, "temp_dataset/annotations", file)

    file_list = os.listdir(image_folder)
    print(file_list[0:5])

    for file in file_list:
         move_files(image_folder, "temp_dataset/images", file)


print(os.getcwd())
splitfolders.ratio("temp_dataset", output="dataset", ratio=(.8, .1, .1))

shutil.rmtree('temp_dataset')