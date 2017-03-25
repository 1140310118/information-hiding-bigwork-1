import sys
import numpy as np

sys.path.append('.\JPG1')
sys.path.append('.\JPG2')
sys.path.append('.\JPG3')
sys.path.append('.\gui')
sys.path.append('.\Steganography')

from encoder.Encoder import *
from encoder.Decoder import *
from gui.gui import *
from Steganography.Jsteg import Jsteg
from Steganography.F3 import *

from div.BmpDiv import *
import DCT

class JPG(BmpDiv):

	def __init__(self):
		BmpDiv.__init__(self)
		self._encoder = Encoder()
		self._decoder = Decoder()

	def init(self,Bmp_file):
		self.setBmpFile(Bmp_file)
		self.data=None

	def write(self,file_out):
		self.divBmp()
		self.split_to_data_shape()
		self.dct()

		self._encoder.encode(self.data, file_out)

	def read(self, file_in):
		self._decoder.decode(file_in)

	def dct(self):
		f=lambda m:DCT.main(m)
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



class SW(JPG):
	#secret writing
	def __init__(self):
		JPG.__init__(self)
		self.jsteg=Jsteg()
		self._mode_W = "JSTEG"
		self._mode_R = "JSTEG"

	def setModeW(self,mode):
		if mode==1:
			self._mode_W = "JSTEG"
		elif mode==2:
			self._mode_W = "F3"
		elif mode==3:
			self._mode_W = "F5"

	def setModeR(self,mode):
		if mode==1:
			self._mode_R = "JSTEG"
		elif mode==2:
			self._mode_R = "F3"
		elif mode==3:
			self._mode_W = "F5"

	def write_init(self,bmp_file):
		self.init(bmp_file)
		self.divBmp()
		self.split_to_data_shape()
		self.dct()

	def write(self,info):
		self._inject(info)
	
	def output_file(self,tmp_file):
		_file = open(tmp_file,'wb')
		self._encoder.encode(self.data, _file)

	def read(self,tmp_file):
		_file = open(tmp_file,'rb')
		self.data=self._decoder.decode(_file)
		return self._uninject()

	def _uninject(self):
		if self._mode_R=="JSTEG":
			return self.jsteg.uninject(self.data)
		elif self._mode_R=="F3":
			a = Stega(None, None, self.data)
			isSuccess, secret_inf = a.decrypt()
			return secret_inf
		else:
			pass

	def get_scale(self):
		try:
			if self._mode_W == "JSTEG":
				return self.jsteg.get_scale(self.data)
			else:
				return "unknown"
		except:
			return 0

	def _inject(self,info):
		if self._mode_W=="JSTEG":
			self.data = self.jsteg.inject(self.data,info)		
			print([i for i in self.data[:1000] if i not in (0,1,-1)])
		elif self._mode_W=="F3":
			a=Stega(self.data,info)
			isSuccess, _len, self.data = a.inject()
		else:
			pass


class ZZWL(GUI):
	def __init__(self):
		GUI.__init__(self)
		self.sw=SW()

	def init(self):
		GUI.init(self)
		self.f5_ratio_W["state"]='disabled'

	def _radio_command(self):
		_mode_R=self._get_type_R()
		_mode_W=self._get_type_W()
		self.sw.setModeW(_mode_W)
		self.sw.setModeR(_mode_R)
		scale=self.sw.get_scale()
		self._set_scale_label(str(scale)+' bits')
		
	def _M_select_bmp_file(self):
		GUI._M_select_bmp_file(self)
		bmp_file=self._get_bmp_path_W()
		self.sw.write_init(bmp_file)
		scale=self.sw.get_scale()
		self._set_scale_label(str(scale)+' bits')

	def _M_write(self):
		bmp_file=self._get_bmp_path_W()
		info=self._get_infor_W()
		if bmp_file=="":
			self._show_message("提示","未选择文件")
		elif info=="":
			self._show_message("提示","请输入待写入信息")
		else:
			self.sw.write_init(bmp_file)
			self.sw.write(info)
			_file=self._savefile()
			self.sw.output_file(_file)

	def _M_read(self):
		tmp_file=self._get_tmp_path_R()
		if tmp_file=="":
			self._show_message("提示","未选择文件")
		else:
			info=self.sw.read(tmp_file)
			self._set_infor_R(info)

		 

if __name__=="__main__":
	a=ZZWL()
	a.init()
	a.mainloop()
		
