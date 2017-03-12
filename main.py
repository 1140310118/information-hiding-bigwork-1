import sys
import numpy as np
sys.path.append('.\JPG1')
sys.path.append('.\JPG2')
sys.path.append('.\JPG3')
sys.path.append('.\gui')

from BmpDiv import BmpDiv
import JPG2

class JPG(BmpDiv):
	def __init__(self):
		BmpDiv.__init__(self)

	def init(self,Bmp_file):
		self.setBmpFile(Bmp_file)

	def main(self):
		self.divBmp()
		self.split_to_data_shape()
		self.dct()

	def dct(self):
		f=lambda m:JPG2.main(m)
		I=len(self.data)
		for i in range(I):
			self.data[i]=f(self.data[i])
		self.data=np.array(self.data).reshape(-1,1)


	def split_to_data_shape(self):
		self.data=[]
		I,J,K=len(self.eximg),len(self.eximg[0]),len(self.eximg[0][0])
		self.shape=[[[0 for k in range(K)] for j in range(J)] for i in range(I)]
		index=0
		for i in range(I):
			for j in range(J):
				for k in range(K):
					self.shape[i][j][k]=index
					self.data.append(self.eximg[i][j][k])
					index+=1


if __name__=="__main__":
	a = JPG()
	a.init("JPG1/test.bmp")
	a.main()
		
