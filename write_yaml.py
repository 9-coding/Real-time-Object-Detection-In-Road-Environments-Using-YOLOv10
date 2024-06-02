import yaml

# yaml file for YOLOv8

data = {
    "train" : '/content/drive/MyDrive/dataset/train/',
    "val" : '/content/drive/MyDrive/dataset/valid/',
    "test" : '/content/drive/MyDrive/dataset/test/',
    "names" : {0: "Animals(Dolls)",
               1: "Person",
               2: "Garbage bag & sacks",
               3: "Construction signs & Parking prohibited board",
               4: "Traffic cone",
               5: "Box",
               6: "Stones on road",
               7: "Pothole on road",
               8: "Filled pothole",
               9: "Manhole"
               }}

with open('./pothole_data.yaml', 'w') as f :
    yaml.dump(data, f)

# check written file
with open('./pothole_data.yaml', 'r') as f :
    lines = yaml.safe_load(f)
    print(lines)