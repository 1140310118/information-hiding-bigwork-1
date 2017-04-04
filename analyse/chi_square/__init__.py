from PIL import Image
import numpy as np
from collections import Counter
import scipy
from scipy.stats import chisquare

class chi_square():
    def __init__(self):
        self.im = None

    def load_bmp(self, bmp_file):
        self.im = Image.open(bmp_file) #文件路径
        img = np.array(self.im)
        arr = img.flatten()
        f = Counter(arr)
        # print(f.values())
        observ = np.array(f.values())
        # print(observ)
        # print(f)
        # observ = f.values()
        test  = scipy.stats.chisquare(observ)
        print(test)
        # print(f)
        # self.w, self.h = self.im.size
        # self.available_info_len = self.w * self.h  # 不是绝对可靠的
        # print("Load>> 可嵌入", self.available_info_len, "bits的信息")

    # def chisquare(self, img):
    #     observ = np.img
    #     test = scipy.stats.chisquare(observ)
    #     print(test)

if __name__=="__main__":
    chi = chi_square()
    chi.load_bmp('timg.jpg')
    # print()
    # observ0 = np.array([25, 38, 40, 20, 37, 44])
    # test0 = scipy.stats.chisquare(observ0)
    # print(test0)
