from PIL import Image
import numpy as np 
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import chisquare

class Chi_square:
	def __init__(self):
		pass

	def load_bmp(self,bmp_file):
		self.im=Image.open(bmp_file)
	
	def get_result(self):
		img=np.array(self.im)
		arr=img.flatten()
		self.f=Counter(arr)
		# h=[]
		# for i in range(256):
		# 	tmp=self.f.get(i)
		# 	if tmp==None:
		# 		h.append(0)
		# 	else:
		# 		h.append(tmp)
		# _h=[]
		# for i in range(128):
		# 	_h.append(h[2*i]+h[2*i+1])
		# r=0
		# for i in range(128):
		# 	if _h[i]!=0:
		# 		r+=(h[2*i]-_h[i])**2/_h[i]
		# a=chisquare(_h,r).pvalue
		# print (a,r)
		return  None#chisquare(self.f.values()).pvalue

	def plot(self):
		x=[]
		for i in range(256):
			tmp=self.f.get(i)
			if tmp==None:
				x.append(0)
			else:
				x.append(tmp)
		plt.figure(figsize=(50,5)) 
		plt.bar(list(range(256)),x,alpha=0.8,color='yellowgreen',width=1)
		plt.show()


if __name__=="__main__":
	chi=Chi_square()
	chi.load_bmp('5.1.14.tiff')
	r=chi.get_result()
	print (r)
	chi.plot()