import json
import os

folder_list = ['test', 'train', 'val']

if not os.path.exists("annotations"):
    os.mkdir("annotations")

for folder in folder_list:
    path = 'dataset/' + folder + '/annotations'
    print(folder)

    if not os.path.exists(path):
        print(f"Error: Annotation folder '{path}' does not exist.")
        continue

    file_list = os.listdir(path)

    for file in file_list:
        file_path = path + '/' + file
        file_name = file[:-10]
        print(file)

        with open(file_path) as f:
            data = json.load(f)
            f = open(f"annotations/{file_name}.txt", 'w')
            for l in range(len(data['annotations'])):
                category_id = data['annotations'][l]['category_id']
                bbox = data['annotations'][l]['bbox']
                #data = str(category_id)#+bbox[0]+bbox[1]+bbox[2]+bbox[3]
                print(category_id, bbox)
                bbox_str = ' '.join(map(str, bbox))
                f.write(str(category_id)+' '+bbox_str+"\n")
            f.close()