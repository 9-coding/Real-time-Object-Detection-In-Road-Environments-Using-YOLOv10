import json
import os

folder_list = ['test', 'train', 'val']

if not os.path.exists("annotations"):
    os.mkdir("annotations")

# xywh형식에서 주어진 데이터셋은 좌상단 xy, YOLO는 중심점 xy 사용.
def find_center(bbox):
    return (bbox[0]*2+bbox[2]) / 2, (bbox[1] * 2 + bbox[3]) / 2

def normalize(x, y, w, h):
    x = x/1280
    y = y/720
    w = w/1280
    h = h/720
    return x, y, w, h

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
                x, y = find_center(bbox)
                point_list = normalize(x, y, bbox[2], bbox[3])
                points = ' '.join(map(str, point_list))
                f.write(str(category_id) + ' ' + points + "\n")
            f.close()


"""
print(path+'/'+file_name + '.png')
            img = cv2.imread('dataset/' + folder + '/images/'+file_name + '.png')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            plt.scatter(bbox[0], bbox[1])
            plt.scatter(bbox[0]+bbox[2], bbox[1]+bbox[3])
            x, y = find_center(bbox)
            #x, y, w, h = normalize(x, y, bbox[2], bbox[3])
            point_list = normalize(x, y, bbox[2], bbox[3])
            print(point_list)
            plt.scatter(x, y)

            plt.show()"""