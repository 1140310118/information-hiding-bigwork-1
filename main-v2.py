import sys
import numpy as np

sys.path.append('.\div')
sys.path.append('.\DCT')
sys.path.append('.\encoder')
sys.path.append('.\gui')
sys.path.append('.\Steganography')

from encoder.Encoder import *
from encoder.Decoder import *
from gui.gui import *
from Steganography.Jsteg import Jsteg
from Steganography.F3 import *
from Steganography.lsb import LSB,LSB_plus,LSB_plus_plus

from div.BmpDiv import *
import DCT
from analyse.rs import RS
from analyse.chi_square import Chi_square

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

def _bin8(_str):
	res=bin(_str)[2:]
	res='0'*(8-len(res))+res
	return res
	
def str2bin(_str):
	return [int(i) for i in ''.join([_bin8(ord(i)) for i in _str])]

def bin2str(_bin):
	_bin=[str(i) for i in _bin]
	res=[]
	_len=int(len(_bin)/8)
	for i in range(_len):
		byte=''.join(_bin[i*8:i*8+8])
		res.append(chr(int(byte,2)))
	return ''.join(res)

class SW1(SW):
	def __init__(self):
		SW.__init__(self)
		self.lsb=LSB()
		self.lsb_plus=LSB_plus()
		self.lsb_plus_plus=LSB_plus_plus()
		self._load_bmp_flag=[False]*5

	def setModeW(self,mode):
		if mode==1:
			self._mode_W = "JSTEG"
		elif mode==2:
			self._mode_W = "F3"
		elif mode==3:
			self._mode_W = "LSB"
		elif mode==4:
			self._mode_W = "LSB+"
		elif mode==5:
			self._mode_W = "LSB++"


	def setModeR(self,mode):
		if mode==1:
			self._mode_R = "JSTEG"
		elif mode==2:
			self._mode_R = "F3"
		elif mode==3:
			self._mode_R = "LSB"
		elif mode==4:
			self._mode_R = "LSB+"
		elif mode==5:
			self._mode_R = "LSB++"
		
	def _write_init(self,bmp_file):
		if self._mode_W in ('JSTEG','F3'):
			self.init(bmp_file)
			self.divBmp()
			self.split_to_data_shape()
			self.dct()
			self._load_bmp_flag[0]=True
			self._load_bmp_flag[1]=True
		elif self._mode_W=='LSB':
			self.lsb.load_bmp(bmp_file)
			self._load_bmp_flag[2]=True
		elif self._mode_W=='LSB+':
			self.lsb_plus.load_bmp(bmp_file)
			self._load_bmp_flag[3]=True
		elif self._mode_W=='LSB++':
			self.lsb_plus_plus.load_bmp(bmp_file)
			self._load_bmp_flag[4]=True

	def write(self,info,bmp_file):
		dic={"JSTEG":0,'LSB':2,'LSB+':3,"LSB++":4}
		if self._load_bmp_flag[dic[self._mode_W]]==False:
			self._write_init(bmp_file)
		
		if self._mode_W in ('Jsteg','F3'):
			self._inject(info)
		elif self._mode_W=='LSB':
			info=str2bin(info)
			self.lsb.write(info)
		elif self._mode_W=='LSB+':
			info=str2bin(info)
			self.lsb_plus.write(info)
		elif self._mode_W=='LSB++':
			info=str2bin(info)
			self.lsb_plus_plus.write(info)

	def output_file(self,tmp_file):
		if self._mode_W in ('Jsteg','F3'):
			_file = open(tmp_file,'wb')
			self._encoder.encode(self.data, _file)
		elif self._mode_W == 'LSB':
			self.lsb.save(tmp_file)
		elif self._mode_W == 'LSB+':
			self.lsb_plus_plus.save(tmp_file)
		elif self._mode_W == 'LSB++':
			self.lsb_plus_plus.save(tmp_file)

	def read(self,tmp_file):
		print (self._mode_R)
		if self._mode_R in ('Jsteg','F3'):
			_file = open(tmp_file,'rb')
			self.data=self._decoder.decode(_file)
			return self._uninject()
		elif self._mode_R == 'LSB':
			self.lsb.load_bmp(tmp_file)
			return bin2str(self.lsb.read())
		elif self._mode_R == 'LSB+':
			self.lsb_plus.load_bmp(tmp_file)
			return bin2str(self.lsb_plus_plus.read())
		elif self._mode_R == 'LSB++':
			self.lsb_plus_plus.load_bmp(tmp_file)
			return bin2str(self.lsb_plus_plus.read())

	def get_scale(self,bmp_file):
		dic={"JSTEG":0,'LSB':2,'LSB+':3,"LSB++":4}
		if self._load_bmp_flag[dic[self._mode_W]]==False:
			self._write_init(bmp_file)
		if self._mode_W == "JSTEG":
			return self.jsteg.get_scale(self.data)
		elif self._mode_W=='LSB':
			return self.lsb.available_info_len
		elif self._mode_W=='LSB+':
			return self.lsb_plus.available_info_len
		elif self._mode_W=='LSB++':
			return self.lsb_plus_plus.available_info_len


class ZZWL(GUI):
	def __init__(self):
		GUI.__init__(self)
		self.sw=SW1()
	
	def _radio_command(self):
		_mode_R=self._get_type_R()
		_mode_W=self._get_type_W()
		print (_mode_R,_mode_W)
		
		self.sw.setModeW(_mode_W)
		self.sw.setModeR(_mode_R)

	def _M_get_scale(self):
		bmp_file=self._get_bmp_path_W()
		info=self._get_infor_W()

		a=len(str2bin(info))
		scale=self.sw.get_scale(bmp_file)
		self._set_scale_label(str(a)+'/'+str(scale)+' bits')

	def _M_select_bmp_file(self):
		GUI._M_select_bmp_file(self)
		bmp_file=self._get_bmp_path_W()
		self.sw._load_bmp_flag=[False]*5

	def _M_write(self):
		bmp_file=self._get_bmp_path_W()
		info=self._get_infor_W()
		if bmp_file=="":
			self._show_message("提示","未选择文件")
		elif info=="":
			self._show_message("提示","请输入待写入信息")
		else:
			self.sw.write(info,bmp_file)
			_file=self._savefile()
			self.sw.output_file(_file)

	def _M_read(self):
		tmp_file=self._get_tmp_path_R()
		if tmp_file=="":
			self._show_message("提示","未选择文件")
		else:
			info=self.sw.read(tmp_file)
			print(info)
			self._set_infor_R(info)

	def _M_analyse(self):
		print ("--分析--")
		bmp_file=self._get_bmp_path_A()
		if bmp_file=="":
			self._show_message("提示","未选择文件")
		else:
			_type_A=self._get_type_A()
			if _type_A==1:
				print ("卡方分析")
				self.chi=Chi_square()
				self.chi.load_bmp(bmp_file)
				result=self.chi.get_result()
				self._set_report_A(result)
			elif _type_A==2:
				print ("rs分析")
				rs=RS()
				rs.load_bmp(bmp_file)
				print (rs.get_RS())
	def _M_analyse_detail(self):
		print ("detail")
		_type_A=self._get_type_A()
		if _type_A==1:
			self.chi.plot()
			

		 

if __name__=="__main__":
	a=ZZWL()
	a.init()
	a.mainloop()
		
