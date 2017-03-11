# coding=utf-8
import math
from enum import Enum
# zigzag扫描方向
Choice = Enum('Choice',('rightTowards', 'rightUp','down','leftDown'))
# print (Choice.rightTowards)
# 量化表
sch_matrix = [[16, 11, 10, 16, 24, 40, 51, 61],
             [12, 12, 14, 19, 26, 58, 60, 55],
             [14, 13, 16, 24, 40, 57, 69, 56],
             [14, 17, 22, 29, 51, 87, 80, 62],
             [18, 22, 37, 56, 68, 109, 103, 77],
             [24, 35, 55, 64, 81, 104, 113, 92],
             [49, 64, 78, 87, 103, 121, 120, 101],
             [72, 92, 95, 98, 112, 100, 103, 99]]
N = 8  # 矩阵边长
input_matrix = [[0 for i in range(N)] for i in range(N)]
output_matrix = [[0 for i in range(N)] for i in range(N)]

# 编码，DCT变换(正向离散余弦变换)
def DCT(input_matirx):
    for p in range(N):
        for q in range(N):
            tmp = 0.0
            if p == 0 :
                coefficient1 = math.sqrt(1.0 / N)
            else:
                coefficient1 = math.sqrt(2.0 / N)
            if q == 0 :
                coefficient2 = math.sqrt(1.0 / N)
            else:
                coefficient2 = math.sqrt(2.0 / N)
            for i in range(N):
                for j in range(N):
                    tmp += input_matirx[i][j]*math.cos((2*i+1)*math.pi*p/(2*N))*math.cos((2*j+1)*math.pi*q/(2*N))
            output_matrix[p][q] = int(round(coefficient1 * coefficient2 * tmp))
    return output_matrix

# 量化
def SCH(input_matrix):
    for i in range(N):
        for j in range(N):
            output_matrix[i][j] = int(input_matrix[i][j] / sch_matrix)
    return output_matrix


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

# Z型扫描
def zigzagScan(input_matrix):
    row = 0
    col = 0
    choice = Choice.rightTowards
    while (row != N - 1 or col != N - 1) :
        print (input_matrix[row][col])
        for case in switch(choice):
            if case('Choice.rightTowards'):
                col+=1
                if row == 0:
                    choice = Choice.leftDown
                else:
                    choice = Choice.rightUp
                break
            if case('Choice.rightUp'):
                row -= 1
                col += 1
                if row == 0 and col != N - 1:
                    choice = Choice.rightTowards
                elif col == N - 1:
                    choice = Choice.down
                else:
                    choice = Choice.rightUp
                break
            if case('Choice.down'):
                row += 1
                if col == 0:
                    choice = Choice.rightUp
                else:
                    choice = Choice.leftDown
                break
            if case('Choice.leftDown'):
                row += 1
                col -= 1
                if col == 0 and row != N - 1:
                    choice = Choice.down
                elif row == N - 1:
                    choice = Choice.rightTowards
                else:
                    choice = Choice.leftDown
                break

matrix = [[1, 5, 3, 9],
          [3, 7, 5, 6],
          [9, 4, 6, 4],
          [7, 3, 1, 3]]

zigzagScan(matrix)













