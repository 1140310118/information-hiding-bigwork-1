from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class GUI:
	def __init__(self):
		self.root=Tk()
		self.root.geometry("500x400")
		self.root.resizable(False, False)
		self.root.title("ZZWL图片隐写小工具-v1.0")
		Frame(self.root,width=500,height=400,bg="#EEEEEE").pack()
	def init(self):
		self._add_widget()
	def _add_widget(self):
		Label(self.root,text="BMP图像").place(x=20,y=40)
		Label(self.root,text="待写入信息").place(x=20,y=80)
		self.bmp_stringVar=StringVar()
		Entry(self.root,textvariable=self.bmp_stringVar,width=40,
			state='readonly',readonlybackground="#FFFFFF").place(x=100,y=40)
		self.infor_entry=Entry(self.root,width=40)
		self.infor_entry.place(x=100,y=80)

		Button(self.root,text="选择",
			command=self._get_infor).place(x=400,y=40)
		
	def _get_infor(self):
		a=filedialog.askopenfilename()
		self.bmp_stringVar.set(a)
		#infor=self.infor_entry.get()
		#messagebox.showinfo("n",infor)
	def mainloop(self):
		self.root.mainloop()

gui=GUI()
gui.init()
gui.mainloop()