from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class _GUI:
	def __init__(self):
		self.root=Tk()
		self.root.geometry("500x280")
		self.root.resizable(False, False)
		self.root.title("ZZWL图片隐写小工具-v1.0")
		self.frame_W=Frame(self.root,width=500,height=400,bg="#FFF")
		self.frame_R=Frame(self.root,width=500,height=400,bg="#FFF")

		self.frame_W.pack()
	def init(self):
		self._add_menu()

	def _M_R(self):
		self.frame_W.pack_forget()
		self.frame_R.pack()
	def _M_W(self):
		self.frame_R.pack_forget()
		self.frame_W.pack()

	def _add_menu(self)	:
		menubar=Menu(self.root)
		function_select_menu=Menu(menubar,tearoff=0)
		function_select_menu.add_command(label="写入",command=self._M_W)
		function_select_menu.add_command(label="读出",command=self._M_R)
		function_select_menu.add_separator()
		function_select_menu.add_command(label="退出")
		
		menubar.add_cascade(label="功能",menu=function_select_menu)
		menubar.add_command(label="版本信息")
		menubar.add_command(label="开发者")
		self.root.config(menu=menubar)	
	def mainloop(self):
		self.root.mainloop()

class GUI_W(_GUI):
	def __init__(self):
		_GUI.__init__(self)
	def init(self):
		_GUI.init(self)
		self._add_widget_W()
	def _add_widget_W(self):
		root=self.frame_W
		self._add_label(root)
		self._add_entry(root)
		self._add_radio(root)
		self._add_button(root)
	def _add_label(self,root):
		Label(root,text="秘密信息的写入",bg="#FFF").place(x=250,y=20,anchor=CENTER)
		Label(root,text="BMP图像",bg="#FFF").place(x=20,y=70)
		Label(root,text="密写方式",bg="#FFF").place(x=20,y=100)
		Label(root,text="可写入信息的容量：",bg="#FFF").place(x=20,y=130)
		Label(root,text="待写入信息",bg="#FFF").place(x=20,y=170)
	def _add_entry(self,root):
		self.bmp_stringVar=StringVar()
		config={'highlightbackground':"#666",
				'highlightthickness':1,
				'relief':FLAT}
		Entry(root,
			textvariable=self.bmp_stringVar,
			width=40,
			state='readonly',
			readonlybackground="#FFFFFF",
			highlightcolor="#00A",
			**config).place(x=100,y=70)

		self.infor_text=Text(root,
							width=45,
							height=4,
							highlightcolor="#00F",
							**config)

		self.infor_text.place(x=100,y=170)
	def _add_radio(self,root):
		self.typeVar = IntVar()
		MODES=[("Jsteg",1),("F3",2),("F5",3)]
		x=100
		config={'bg':"#FFF",'relief':FLAT}
		text,mode=MODES[0]
		r=Radiobutton(root,
					text=text,
					variable=self.typeVar,
					value=mode,
					**config)
		r.place(x=100,y=100)
		r.select()
		for text,mode in MODES[1:]:
			x+=60
			Radiobutton(root,
						text=text,
						variable=self.typeVar,
						value=mode,
						**config).place(x=x,y=100)
			
	def _add_button(self,root):
		Button(root,
			text="选择文件",
			command=self._M_select_bmp_file,
			relief=GROOVE).place(x=400,y=70)
		Button(root,
			text="  写入图片  ",
			height=1,
			relief=GROOVE).place(x=280,y=235)
		Button(root,
			text="  退出  ",
			height=1,
			relief=GROOVE).place(x=380,y=235)
		
	def _M_select_bmp_file(self):
		a=filedialog.askopenfilename()
		self.bmp_stringVar.set(a)

	def _get_infor(self):
		return self.infor_text.get('1.0',END)

	def _get_type(self):
		return self.typeVar.get()

class GUI_WR(GUI_W):
	def __init__(self):
		GUI_W.__init__(self)
	def init(self):
		GUI_W.init(self)
		self._add_widget_R()
	def _add_widget_R(self):
		root=self.frame_R
	

class GUI(GUI_WR):
	def __init__(self):
		GUI_WR.__init__(self)

gui=GUI()
gui.init()
gui.mainloop()