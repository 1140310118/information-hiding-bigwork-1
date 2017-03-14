import sys
import numpy as np
from JPG3.Encoder import *
from JPG3.Decoder import *
# sys.path.append('.\JPG1')
# sys.path.append('.\JPG2')
# sys.path.append('.\JPG3')
# sys.path.append('.\gui')

from JPG1.BmpDiv import *
import JPG2

class JPG(BmpDiv):

	def __init__(self):
		BmpDiv.__init__(self)
		self._mode = None

	def setMode(self,mode):
		self._mode = mode

	def init(self,Bmp_file):
		self.setBmpFile(Bmp_file)
		self._encoder = Encoder()
		self._decoder = Decoder()

	def write(self,file_out):
		self.divBmp()
		self.split_to_data_shape()
		self.dct()
		
		self._encoder.encode(self.data, file_out)

	def read(self, file_in):
		self._decoder.decode(file_in)

	def get_scale(self):
		pass

	def dct(self):
		f=lambda m:JPG2.main(m)
		I=len(self.data)
		for i in range(I):
			self.data[i]=f(self.data[i])
		self.data=np.array(self.data).astype(int).reshape(1,-1)[0]
		self.data=list(self.data)
		self.data=[127 if i > 127 else i for i in self.data]


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
	file_out = open("F:\\test.jpg",'wb')
	a.write(file_out)
		
