from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class GUI:
	def __init__(self):
		self.root=Tk()
		self.root.geometry("500x280")
		self.root.resizable(False, False)
		self.root.title("ZZWL图片隐写小工具-v1.0")
		Frame(self.root,width=500,height=400,bg="#EEE").pack()
	def init(self):
		menubar=Menu(self.root)
		function_select_menu=Menu(menubar,tearoff=0)
		function_select_menu.add_command(label="隐写")
		function_select_menu.add_command(label="读出秘密信息")
		menubar.add_cascade(label="功能",menu=function_select_menu)
		#menubar.add_separator()
		menubar.add_command(label="版本信息")
		menubar.add_command(label="开发者")
		menubar.add_command(label="退出")
		self.root.config(menu=menubar)
		self._add_widget()
	def _add_widget(self):
		self._add_label()
		self._add_entry()
		self._add_radio()
		self._add_button()
	def _add_label(self):
		Label(self.root,text="BMP图像").place(x=20,y=40)
		Label(self.root,text="密写方式").place(x=20,y=80)
		Label(self.root,text="可写入信息的容量：").place(x=20,y=120)
		Label(self.root,text="待写入信息").place(x=20,y=160)
	def _add_entry(self):
		self.bmp_stringVar=StringVar()
		Entry(self.root,textvariable=self.bmp_stringVar,width=40,
			state='readonly',readonlybackground="#FFFFFF",
			highlightbackground="#666",
			highlightthickness=1,highlightcolor="#00F",relief=FLAT
			).place(x=100,y=40)
		self.infor_text=Text(self.root,width=45,height=4,highlightbackground="#666",
			highlightthickness=1,highlightcolor="#00F",relief=FLAT)
		self.infor_text.place(x=100,y=160)
	def _add_radio(self):
		v=StringVar()
		MODES=[("Jsteg",1),("F3",2),("F5",3)]
		x=100
		for text,mode in MODES:
			Radiobutton(self.root,text=text,variable=v,value=mode).place(x=x,y=80)
			x+=60
	def _add_button(self):
		Button(self.root,text="选择",
			command=self._get_infor,relief=GROOVE).place(x=400,y=40)
		Button(self.root,text="  写入图片  ",
			height=1,relief=GROOVE).place(x=360,y=235)
		
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