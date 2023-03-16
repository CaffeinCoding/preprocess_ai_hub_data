import os
import json

save_label_dir = "./result/label"
save_face_image = "./result/face_image"

if not os.path.exists(save_label_dir):
    os.makedirs(save_label_dir)

if not os.path.exists(save_face_image):
    os.makedirs(save_face_image)

data_path = "./data"

result = []
check = os.listdir(data_path)
for i in check:
    if os.path.isdir(os.path.join(data_path, i)):
        a = os.listdir(os.path.join(data_path, i))
        for j in a:
            if os.path.isdir(os.path.join(data_path, i, j)):
                b = os.listdir(os.path.join(data_path, i, j))
                for k in b:
                    if os.path.isdir(os.path.join(data_path, i, j, k)):
                        c = os.listdir(os.path.join(data_path, i, j, k))
                        for p in c:
                            if os.path.isdir(os.path.join(data_path, i, j, k, p)):
                                d = os.listdir(os.path.join(
                                    data_path, i, j, k, p))
                                for t in d:
                                    if not os.path.isdir(os.path.join(data_path, i, j, k, p, t)):
                                        result.append(t)
                            else:
                                result.append(p)
                    else:
                        result.append(k)
            else:
                result.append(j)
    else:
        result.append(i)


print(check)
print(len(check))
print(len(result))
