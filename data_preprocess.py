import os
import json


class DataPreprocess:

    def __init__(self):
        save_label_dir = "./result/label"
        save_face_image = "./result/face_image"

        if not os.path.exists(save_label_dir):
            os.makedirs(save_label_dir)

        if not os.path.exists(save_face_image):
            os.makedirs(save_face_image)

    def savePath(self, path_list, file_name_list, path, file_name):
        file_name, file_ext = os.path.splitext(file_name)

        if file_ext != '.zip':
            path_list.append(path)
            file_name_list.append(file_name)

    def getDataPath(self, data_path):
        paths = []
        file_names = []
        check = os.listdir(data_path)
        for i in check:
            path_i = os.path.join(data_path, i)
            if os.path.isdir(os.path.join(data_path, i)):
                a = os.listdir(os.path.join(data_path, i))
                for j in a:
                    path_j = os.path.join(data_path, i, j)
                    if os.path.isdir(os.path.join(data_path, i, j)):
                        b = os.listdir(os.path.join(data_path, i, j))
                        for k in b:
                            path_k = os.path.join(data_path, i, j, k)
                            if os.path.isdir(os.path.join(data_path, i, j, k)):
                                c = os.listdir(
                                    os.path.join(data_path, i, j, k))
                                for p in c:
                                    path_p = os.path.join(
                                        data_path, i, j, k, p)
                                    if os.path.isdir(path_p):
                                        d = os.listdir(os.path.join(
                                            data_path, i, j, k, p))
                                        for t in d:
                                            path_t = os.path.join(
                                                data_path, i, j, k, p, t)
                                            if not os.path.isdir(path_t):
                                                self.savePath(
                                                    paths, file_names, path_t, t)
                                    else:
                                        self.savePath(
                                            paths, file_names, path_p, p)
                            else:
                                self.savePath(paths, file_names, path_k, k)
                    else:
                        self.savePath(paths, file_names, path_j, j)
            else:
                self.savePath(paths, file_names, path_i, i)

        return paths, file_names

    def saveLabelData(self, file_name):
        save_label_txt = "result/label/custom_face_label.txt"
        save_root_dir = "result/face_image"
        save_file_dir = save_root_dir + "/" + file_name + ".jpg"

        # with open(save_label_txt, "a", encoding="utf-8") as f:
        #     f.write()


data_path = "./data"
dp = DataPreprocess()
paths, file_names = dp.getDataPath(data_path)

print(len(paths))
print(file_names)
# print(result)
