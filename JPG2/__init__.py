# coding=utf-8
import math

# 量化表
sch_matrix = [[16, 11, 10, 16, 24, 40, 51, 61],
             [12, 12, 14, 19, 26, 58, 60, 55],
             [14, 13, 16, 24, 40, 57, 69, 56],
             [14, 17, 22, 29, 51, 87, 80, 62],
             [18, 22, 37, 56, 68, 109, 103, 77],
             [24, 35, 55, 64, 81, 104, 113, 92],
             [49, 64, 78, 87, 103, 121, 120, 101],
             [72, 92, 95, 98, 112, 100, 103, 99]]
# zigzag矩阵
index_matrix = [[0, 1, 5, 6, 14, 15, 27, 28],
                [2, 4, 7, 13, 16, 26, 29, 42],
                [3, 6, 12, 17, 25, 30, 41, 43],
                [9, 11, 18, 24, 31, 40, 44, 53],
                [10, 19, 23, 32, 39, 45, 52, 54],
                [20, 22, 33, 38, 46, 51, 55, 60],
                [21, 34, 37, 47, 50, 56, 59, 61],
                [35, 36, 48, 49, 57, 58, 62, 63]]

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


def zigzagScan(input_matrix):
    B = [0] * 64
    for i in range(N):
        for j in range(N):
            index = index_matrix[i][j]
            B[index] = input_matrix[i][j]
    return B












