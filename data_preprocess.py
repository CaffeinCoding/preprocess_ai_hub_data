import os
import json
import re
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd
from PIL import Image
import glob

# Age
# a : 0 ~ 6
# b : 7 ~ 12
# c : 13 ~ 19
# d : 20 ~ 30
# e : 31 ~ 45
# f : 46 ~ 55
# g : 56 ~ 66
# h : 67 ~ 80

# Gender
# GF, F, S : 1
# GM, M, D : 0


class DataPreprocess:

    def __init__(self):
        self.save_label_dir = "./result/label"
        self.save_face_image_path = "./custom_face_image"
        self.pattern_digit = r'[0-9]+'
        self.data_frame = pd.DataFrame(
            columns=["count", "path", "age", "gender"])
        self.age_map = {
            'a': 0,
            'b': 7,
            'c': 13,
            'd': 20,
            'e': 31,
            'f': 46,
            'g': 56,
            'h': 67,
        }

        if not os.path.exists(self.save_label_dir):
            os.makedirs(self.save_label_dir)

        if not os.path.exists(self.save_face_image_path):
            os.makedirs(self.save_face_image_path)

    def getGender(self, gender):
        gender = re.sub(self.pattern_digit, "", gender)
        if gender == "GF" or gender == "F" or gender == "S":
            gender = 1
        else:
            gender = 0
        return gender

    def getAge(self, age, default_age):
        age_id = re.sub(self.pattern_digit, "", age)
        age_num = int(re.sub(r'[^0-9]+', '', age))
        age = self.age_map[age_id]
        age += (6*age_num - 6)/7
        age = round(age, 1)
        if age >= default_age:
            age = default_age
        return float(age)

    def getJsonData(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    # def getImage(self, file_path):
    #     img_arr = np.fromfile(file_path, np.uint8)
    #     img = cv2.imdecode(img_arr, cv2.COLOR_BGR2RGB)
    #     return img

    def getImage(self, file_path):
        img = Image.open(file_path).convert("RGB")
        return img

    # def cropImage(self, img, x, y, range):
    #     x = int(x)
    #     if x < 0:
    #         x = 0
    #     y = int(y)
    #     if y < 0:
    #         y = 0
    #     range = int(range)
    #     img = img[y:y+range, x:x+range]
    #     img = cv2.resize(img, (224, 224))
    #     return img

    def cropImage(self, img, x, y, range):
        x = int(x)
        if x < 0:
            x = 0
        y = int(y)
        if y < 0:
            y = 0
        range = int(range)
        img = img.crop((x, y, x+range, y+range))
        img = img.resize((224, 224), Image.LANCZOS)
        return img

    def savePath(self, path_list, file_name_list, path, file_name):
        name, file_ext = os.path.splitext(file_name)

        if file_ext == '.jpg' or file_ext == '.json' or file_ext == '.JPG' or file_ext == '.png' or file_ext == '.PNG':
            path_list.append(os.path.join(path, file_name))
            file_name_list.append(name)

    # def setImgPath(self, path_list):
    #     img_paths = []
    #     for path in path_list:
    #         img_path = re.sub("label", "data", path)
    #         img_path = re.sub("json", "jpg", img_path)
    #         img_path = re.sub("TL", "TS", img_path)
    #         img_paths.append(img_path)
    #     return img_paths

    def setImgPath(self, image_paths, image_file_names, label_file_names):
        img_paths = []
        for file_name in label_file_names:
            idx = image_file_names.index(file_name)
            img_paths.append(image_paths[idx])
        return img_paths

    def getDataPath(self, root_path):
        paths = []
        file_names = []
        for (path, dir, files) in os.walk(root_path):
            for file in files:
                self.savePath(paths, file_names, path, file)
        return paths, file_names

    # def saveImageData(self, file_name, img):
    #     save_data_root = "custom_face_image"
    #     save_data_path = save_data_root + "/" + file_name + ".jpg"
    #     cv2.imwrite(save_data_path, img)

    def saveImageData(self, file_name, img):
        save_data_root = "custom_face_image"
        save_data_path = save_data_root + "/" + file_name + ".jpg"
        img.save(save_data_path, format="jpeg", quality=100)

    def saveLabelData(self, file_name, count, age, gender):
        save_file_dir = self.save_face_image_path + "/" + file_name + ".jpg"

        self.data_frame.loc[len(self.data_frame)] = {
            'count': count, 'path': save_file_dir, 'age': age, 'gender': gender}

    def saveLabel(self):
        save_label_txt = "result/label/custom_face_label.txt"
        self.data_frame.to_csv(save_label_txt, sep=" ",
                               header=False, index=False)


class BeforeData:
    family_id = ""
    default_age = ""
    gender = ""
    flag = False


data_path = "./data"
label_path = "./label"
dp = DataPreprocess()
label_paths, label_file_names = dp.getDataPath(label_path)
image_paths, image_file_names = dp.getDataPath(data_path)
data_paths = dp.setImgPath(image_paths, image_file_names, label_file_names)
before_data_flag = False
before_data = BeforeData()
count = 0

print(len(data_paths))

# print(data_paths)

for idx in tqdm(range(len(data_paths))):
    label_features = label_paths[idx].split("_")
    if "AGE" in label_features:
        json_data = dp.getJsonData(label_paths[idx])
        file_name = label_file_names[idx]
        family_id = label_features[0]
        member = json_data['member'][0]
        default_age = label_features[3]
        age = member['age_class']
        gender = label_features[2]

        if not before_data.flag:
            before_data.family_id = family_id
            before_data.default_age = default_age
            before_data.gender = gender
            before_data.flag = True

        if before_data.family_id != family_id or before_data.default_age != default_age or before_data.gender != gender:
            count += 1
            before_data.family_id = family_id
            before_data.default_age = default_age
            before_data.gender = gender

        img = dp.getImage(data_paths[idx])
        age = dp.getAge(age, int(default_age))
        gender = dp.getGender(gender)

        img_bb = member['regions'][0]['boundingbox'][0]

        img = dp.cropImage(img, img_bb["x"], img_bb["y"], img_bb["w"])

        dp.saveImageData(file_name, img)
        dp.saveLabelData(file_name, count, age, gender)

dp.saveLabel()
