# written by 0oSpacebaro0 2017.03.12
import os
from logger import logger
import cv2
import numpy


class BmpDiv:
    def __init__(self):
        """
        self.img    :存储原始bmp图像的像素矩阵信息。type = <class 'numpy.ndarray'>
        self.eximg  :存储self.img 扩展后分割成 元素为 8*8 ndarray 的矩阵。
                    矩阵大小为 self.pheight * self.pwidth * self.sdepth. type = list
                    其每个元素为 8*8矩阵，类型与img相同
        self.pheight 与 self.pwidth 的‘p'代表 piece
        self.sheight 与 self.swidth 的’s'代表 source

        """
        self.img = None
        self.eximg = None
        self.filename = ""
        self.swidth = 0
        self.sheight = 0
        self.sdepth = 0
        self.pheight = 0
        self.pwidth = 0

    def __isFile(self, filename):
        if not os.path.isfile(filename):
            errmsg = 'NO found file %s' % filename
            logger.error(errmsg)
            return False
        infmsg = 'Get file name : %s' %filename
        logger.info(infmsg)
        return True

    def __isBmpFile(self, filename):
        if self.__isFile(filename):
            with open(filename, "rb") as f:
                if f.read(2) != b'BM':
                    errmsg = '%s is no bmp file' % filename
                    logger.error(errmsg)
                    return False
            infmsg = 'File "%s" is Bitmap file' % filename
            logger.info(infmsg)
            return True
        return False

    def __getBmpFile(self, filename,show_flag):
        if not self.__isBmpFile(filename):
            return None
        img = cv2.imread(filename)
        if show_flag:
            cv2.namedWindow("Image")
            cv2.imshow("Image", img)
            cv2.waitKey()
        return img

    def setBmpFile(self, filename,flag=False):
        img = self.__getBmpFile(filename,flag)
        if isinstance(img, numpy.ndarray):
            self.filename = filename
            self.img = img
            self.sheight, self.swidth, self.sdepth = img.shape
            infmsg = "The image size : %d * %d , depth : %d " \
                     % (self.sheight, self.swidth, self.sdepth)
            logger.info(infmsg)
            return True
        else:
            return False

    def divBmp(self):
        if self.img is None:
            return False
        self.pheight = int(self.sheight / 8 + 0.875)
        self.pwidth = int(self.swidth / 8 + 0.875)
        exheight = self.pheight * 8
        exwidth = self.pwidth * 8
        expandimg = numpy.zeros((self.pheight * 8, self.pwidth * 8, self.sdepth))
        expandimg[:self.sheight, :self.swidth, :self.sdepth] = self.img
        infmsg = "The image is expanded to %d * %d " \
                 "and divided into %d blocks in height, %d blocks in width" \
                 % (exheight, exwidth, self.pheight, self.pwidth)
        logger.info(infmsg)
        pieces = [[[[] for depth in range(self.sdepth)] for col in range(self.pwidth)] for row in range(self.pheight)]
        # pieces = numpy.zeros((self.pheight,self.pwidth,self.sdepth))
        for i in range(self.pheight):
            for j in range(self.pwidth):
                for k in range(self.sdepth):
                    pieces[i][j][k] = expandimg[i*8:i*8+8, j*8:j*8+8, k]
        self.eximg = pieces
        return True

if __name__ == '__main__':
    a = BmpDiv()
    if a.setBmpFile("test.bmp"):
        a.divBmp()
    """
    img1 = self.img[:, :, 1]
    cv2.namedWindow("img1")
    cv2.imshow("img1", img1)
    cv2.waitKey()
    img2 = self.img[:, :, 0]
    cv2.namedWindow("img2")
    cv2.imshow("img2", img2)
    cv2.waitKey()
    img3 = self.img[:, :, 2]
    cv2.namedWindow("img3")
    cv2.imshow("img3", img3)
    cv2.waitKey()
    """

    """
    print(a.img[0][0])
    print(a.pheight, a.pwidth)
    """


