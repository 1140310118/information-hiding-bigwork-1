import sys
import math
import numpy as np
from PIL import Image
# import time
import random

"""
RS分析方法的核心
	由于LSB密写仅用到了F(1)翻转，而没有用到F(-1)翻转，
所以当用F(-1)翻转或F(1)翻转去处理密写图像时，参数呈现
不对称性。通过这种不对称性，我们可以估计密写率。

【参考】以下参考自  
		吕述望等.对 RS攻击的分析及抗RS攻击的隐写算法.中山大学学报(自然科学版).2004-11
		百度文库链接 https://wenku.baidu.com/view/b87eac0a581b6bd97f19ea9d.html?re=view

RS方法的原理
	f(G)=∑|x(i+1)-x(i)|
	相关文献指出，自然图像的像素点与其相邻像素的差值近似服从广义高斯分布。
	

(1) 嵌入率p=0时，证明Rm=R-m,Sm=S-m
	设G=(x(1),x(2)),M=(0,1)
													(0,1)	(0,-1)
	则 	1.|x(1)-x(2)|=0								Rm 		R-m
		2.|x(1)-x(2)|=1,x(1) =x(2)^1				Sm 		R-m
						x(1)!=x(2)^1				Rm 		S-m
		3.|x(1)-x(2)|>1,x(1)>x(2),x(2)为偶数		Sm 		R-m
						x(1)>x(2),x(2)为奇数		Rm 		S-m
		4.x(1)<x(2),同3

	得 Rm=R-m,Sm=S-m.类似地，取M=(1,0),(0,0),(1,1)也可得到Rm=R-m,Sm=S-m，
	因此，有Rm=R-m,Sm=S-m。

(2) 嵌入率p的影响
	嵌入率为p,令q=1-p,则像素值改变的概率为p/2。
	取 m=(0,1),F(m)=(F(1),F(0)),F(-m)=(F(-1),F(0))
	令P1,P2,P34为(1)中四种情况发生的概率，则
		1.P{R->R} = [(p/2)*(p/2)+(1-p/2)*(1-p/2)]P1 =(1/2+q**2/2)P1
		  P{R->S} = (1/2-q**2/2)P1
		2.1 P{S->S} = (1/2+q**2/2)P2/2
			P{S->R} = (1/2-q**2/2)P2/2
		2.2 P{R->R} = (1/2+q**2/2+qp/2)P2/2
			P{R->S} = (p**2/2+qp/2)P2/2
		3.1 与 4.1 	P{R->R} = [1/2+q**2/2+qp/2]P34/2
					P{R->S} = [p**2/2+qp/2]P34/2
		3.2 与 4.2 	P{S->S} = [1/2+q**2/2+qp/2]P34/2
					P{S->R} = [p**2/2+qp/2]P34/2
		故 P{Rm}-P{Sm}=q**2*P1+pq*P2/2, 当p=1时，P{Rm}=P{Sm}

"""


# index_matrix=[[0,  1,  5,  6,  14, 15, 27, 28],
# 				[2,  4,  7,  13, 16, 26, 29, 42],
# 				[3,  8,  12, 17, 25, 30, 41, 43],
# 				[9,  11, 18, 24, 31, 40, 44, 53],
# 				[10, 19, 23, 32, 39, 45, 52, 54],
# 				[20, 22, 33, 38, 46, 51, 55, 60],
# 				[21, 34, 37, 47, 50, 56, 59, 61],
# 				[35, 36, 48, 49, 57, 58, 62, 63]]


m=[random.randint(0,1) for i in range(64)]
m=np.array(m).astype(int)


class RS:
	def __init__(self):
		pass

	def load_bmp(self,bmp_file):
		self.im=Image.open(bmp_file)
		self.w,self.h=self.im.size
		print (">> 加载图片，图片尺寸：",self.w,"x",self.h)

	def _RS_init(self):
		self.Rm=0
		self.R_m=0
		self.R_m=0
		self.S_m=0

	def get_RS(self):
		print (">> 进行分析")
		self._RS_init()
		_l=8
		row=math.ceil(self.w/_l)
		column=math.ceil(self.h/_l)
		for i in range(row):
			for j in range(column):
				box=(i*_l,j*_l,(i+1)*_l,(j+1)*_l)
				region=self.im.crop(box)
				self._inc_rs(region)
		return (self.Rm,self.R_m,self.Sm,self.S_m)

	def analyse(self):
		pass


	def get_RS_map(self):
		# print ("rate,R-,R,S,S-")
		res=[]
		for i in range(100):
			R,R_,S,S_=self._get_RS_by_rate(i/100)
			_tmp=(i/100,R_,R,S,S_)
			print (_tmp)
			res.append(_tmp)

		return res
		
	def _get_RS_by_rate(self,rate):
		self.Rm=0
		self.R_m=0
		self.Sm=0
		self.S_m=0
		_l=8
		row=math.ceil(self.w/_l)
		column=math.ceil(self.h/_l)
		for i in range(row):
			for j in range(column):
				box=(i*_l,j*_l,(i+1)*_l,(j+1)*_l)
				region=self.im.crop(box)
				self._random_inject_and_inc_rs(region,rate)
		return (self.Rm,self.R_m,self.Sm,self.S_m)
				
	def _inc_rs(self,region):
		arr=np.array(region)
		sequence=self._zigzagScan(arr)

		self._modify_rs(sequence)

	def _random_inject_and_inc_rs(self,region,rate):
		half_rate=rate/2
		arr=np.array(region)
		sequence=self._zigzagScan(arr)
		for i in range(len(sequence)):
			p=random.random()
			if p<half_rate:
				sequence[i]^=1
		self._modify_rs(sequence)

	def _modify_rs(self,sequence):
		"""
		根据sequence修改RS的值
		"""
		r1=self._get_relativity(sequence)
		r2=self._get_relativity(self._Fm(sequence, m))
		r3=self._get_relativity(self._Fm(sequence,-m))

		if r1<r2:
			self.Rm+=1
		elif r1>r2:
			self.Sm+=1
		if r1<r3:
			self.R_m+=1
		elif r1>r3:
			self.S_m+=1

	def _get_relativity(self,sequence):
		"""
		得到像素相关性
		"""
		a=np.abs(np.array(sequence)[1:]-np.array(sequence)[:1])
		return np.sum(a)

	def _Fm(self,sequence,m):
		"""
		由m定义的翻转
		"""
		# [0,1,-1]
		# x^0,x^1,(x-1)^1+1
		# ((x+a)^b)-a
		a=np.floor(m/2).astype(int)
		b=np.abs(m).astype(int)
		return ((sequence+a)^b)-a

	def _zigzagScan(self,m):
		"""
		Z字形扫描
		"""
		sequence = np.zeros(64,).astype(int)
		for i in range(8):
			for j in range(8):
				index = index_matrix[i][j]
				sequence[index] = m[i,j]
		return sequence



if __name__=="__main__":
	rs=RS()
	rs.load_bmp("5.1.14.bmp")
	rs.get_RS_map()

 
