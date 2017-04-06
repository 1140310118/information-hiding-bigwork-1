from PIL import Image
import math
import numpy as np
from collections import Counter
import random


class LSB:
	def __init__(self):
		self.im=None
 
	def load_bmp(self,bmp_file):
		self.im=Image.open(bmp_file)
		self.w,self.h=self.im.size
		self.available_info_len=self.w*self.h # 不是绝对可靠的
		self.d=0 # 为了计算PSNR
		print (">> 加载图片，图片尺寸：",self.w,"x",self.h)
		print ("	可嵌入",self.available_info_len,"bits的信息")
 
	def write(self,info):
		"""先嵌入信息的长度，然后嵌入信息"""
		info=self._set_info_len(info)
		info_len=len(info)
		info_index=0
		im_index=0
		while True:
			if info_index>=info_len:
				break
			data=info[info_index]
			x,y=self._get_xy(im_index)
			self._write(x,y,data)
			info_index+=1
			im_index+=1
		print (">> LSB complete.")
		print ("	PSNR:",self.get_PSNR())
		print ("	嵌入率:",self.get_RATE(len(info))*100,"%")
 
	def save(self,filename):
		self.im.save(filename)
 
	def read(self):
		"""先读出信息的长度，然后读出信息"""
		_len,im_index=self._get_info_len()
		info=[]
		for i in range(im_index,im_index+_len):
			x,y=self._get_xy(i)
			data=self._read(x,y)
			info.append(data)
		return info
 
	#===============================================================#
	def _get_xy(self,l):
		return l%self.w,int(l/self.w)
 
	def _set_info_len(self,info):
		l=int(math.log(self.available_info_len,2))+1
		info_len=[0]*l
		_len=len(info)
		info_len[-len(bin(_len))+2:]=[int(i) for i in bin(_len)[2:]]
		return info_len+info
 
	def _get_info_len(self):
		l=int(math.log(self.w*self.h,2))+1
		len_list=[]
		for i in range(l):
			x,y=self._get_xy(i)
			_d=self._read(x,y)
			len_list.append(str(_d))
		_len=''.join(len_list)
		_len=int(_len,2)
		return _len,l
 
	def _write(self,x,y,data):
		origin=self.im.getpixel((x,y))
		lower_bit=origin%2
		if lower_bit==data:
			pass
		elif (lower_bit,data) == (0,1):
			self.d+=1
			self.im.putpixel((x,y),origin+1)
		elif (lower_bit,data) == (1,0):
			self.d+=1
			self.im.putpixel((x,y),origin-1)
 
	def _read(self,x,y):
		data=self.im.getpixel((x,y))
		return data%2

	def get_PSNR(self):
		PSNR=-10*math.log(self.d/255**2/self.w/self.h,10)
		return PSNR

	def get_RATE(self,_len):
		return _len/self.w/self.h/8


class LSB_plus(LSB):
	def __init__(self):
		LSB.__init__(self)

	def load_bmp(self,bmp_file):
		self.im=Image.open(bmp_file)
		self.w,self.h=self.im.size
		self._get_available_info_len(self.w,self.h)
		self.d=0 # 为了计算PSNR
		print (">> 加载图片，图片尺寸：",self.w,"x",self.h)
		print (">> 大约可嵌入",self.available_info_len,"bits的信息") 
		# 这个数值基于一个假设：图像的像素值随机排列
 
	def _get_available_info_len(self,w,h):
		alpha=1
		img=np.array(self.im)
		arr=img.flatten()
		f=Counter(arr)
		for i in range(128):
			if f[2*i]+f[2*i+1]==0:
				continue	
			rate=2*f[2*i+1]/(f[2*i]+f[2*i+1])	
			if rate==0:
				continue
			if alpha > rate:
				alpha = rate
		self.available_info_len=int(alpha*self.w*self.h)

	def write(self,info):
		"""
		先嵌入信息的长度，然后嵌入信息;
		嵌入时统计，并进行直方图补偿。
		"""
		_offset=[0]*128

		info=self._set_info_len(info)
		info_len=len(info)
		info_index=0
		im_index=0
		while True:
			if info_index>=info_len:
				break
			data=info[info_index]
			x,y=self._get_xy(im_index)
			self._write(x,y,data,_offset)
			info_index+=1
			im_index+=1

		# 补偿
		for i in range(im_index,self.w*self.h):
			x,y=self._get_xy(i)
			origin=self._read(x, y)
			if _offset[int(origin/2)]<0:
				self._put(x,y,origin+1)
			elif _offset[int(origin/2)]>0:
				self._put(x,y,origin-1)

		print (">> LSB+ complete,PSNR:",self.get_PSNR())

	def _put(self,x,y,data):
		self.d+=1
		self.im.putpixel((x,y),data)

	def _write(self,x,y,data,_offset):
		origin=self.im.getpixel((x,y))
		lower_bit=origin%2
		if lower_bit==data:
			pass
		elif (lower_bit,data) == (0,1):
			self.d+=1
			self.im.putpixel((x,y),origin+1)
			_offset[int(origin/2)]+=1
		elif (lower_bit,data) == (1,0):
			self.d+=1
			self.im.putpixel((x,y),origin-1)
			_offset[int(origin/2)]-=1

 
class LSB_plus_plus(LSB):
	def __init__(self):
		LSB.__init__(self)

	def _write(self,x,y,data):
		origin=self.im.getpixel((x,y))
		lower_bit=origin%2
		if lower_bit==data:
			pass
		else:
			self.d+=1
			if origin==0:
				self.im.putpixel((x,y),origin+1)
			elif origin==255:
				self.im.putpixel((x,y),origin-1)
			elif random.random()>0.5:
				self.im.putpixel((x,y),origin+1)
			else:
				self.im.putpixel((x,y),origin-1)
		# elif (lower_bit,data) == (1,0):
		#	 self.d+=1
		#	 self.im.putpixel((x,y),origin-1)

if __name__=="__main__":
	lsb=LSB()
	# 写
	lsb.load_bmp('../_data/2.bmp')
	info1=[0,1,0,1,1,0,1,0]
	lsb.write(info1)
	lsb.save('lsb.bmp')
	# 读
	lsb.load_bmp('lsb.bmp')
	info2=lsb.read()
	print (info2)
	
	# a=LSB_plus()
	# a.load_bmp('../_data/1.bmp')