import pandas as pd

# 참고 https://mizykk.tistory.com/55


class FindSameImg:
    def __init__(self):
        self.label_path = "./result/label/custom_face_label.txt"

    def load_img_df(self):
        df = pd.read_csv(self.label_path, sep=" ", names=[
                         "count", "path", "age", "gender"], header=None)
        return df


fsi = FindSameImg()
df = fsi.load_img_df()

print(df.head())
