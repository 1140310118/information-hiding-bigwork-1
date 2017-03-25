import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import *

class PLOT:
	def __init__(self):
		self.root=Tk()
	def init(self):
		matplotlib.use("TkAgg")
		self._root_init()
		self._add_widget()
	def mainloop(self):
		self.root.mainloop()

	def _root_init(self):
		self.root.f = Figure(figsize=(5,4), dpi=100) 
		self.root.canvas = FigureCanvasTkAgg(self.root.f, master=self.root)
		self.root.canvas.show()
		self.root.canvas.get_tk_widget().grid(row=0, columnspan=3)  

	def _add_widget(self):
		Label(self.root,text='请输入样本数量：').grid(row=1,column=0)
		self._inputEntry=Entry(self.root)
		self._inputEntry.grid(row=1,column=1)
		self._inputEntry.insert(0,'50')
		Button(self.root,text='画图',command=self.drawPic).grid(row=1,column=2,columnspan=3)

	def drawPic(self):
		try:
			sampleCount=int(self._inputEntry.get())
		except:
			sampleCount=50 
			print ("请输入整数")
			self._inputEntry.delete(0,END)
			self._inputEntry.insert(0,'50')
		self.root.f.clf()
		self.root.a=self.root.f.add_subplot(111)

		x=np.random.randint(0,100,size=sampleCount)
		y=np.random.randint(0,100,size=sampleCount)

		color=['b','r','y','g']
		self.root.a.scatter(x,y,s=3,color=color[np.random.randint(len(color))])
		self.root.a.set_title('Demo: Draw N Random Dot')
		self.root.canvas.show()

if __name__=="__main__":
	plot=PLOT()
	plot.init()
	plot.mainloop()