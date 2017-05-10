#!/usr/bin/python
import Tkinter as tk
import tkMessageBox
import pickle
import sched, time
from tnt2lib import xor_crypt

__version__ = "0.0.1"
__author__ = "Tshaba Phomolo Benedict"
notes_file = "notes.db"

class MyApp(object):
	def __init__(self,master):
		self.master = master
		self.master.title("TNT2")
		self.master.geometry("600x400")
		self.editor = Editor(self.master)
		self.menubar = MenuBar(self.master)
		self.editor.autoSave()
		self.master.mainloop()

class MenuBar(object):
	def __init__(self,master):
		self.master = master
		self.menubar = tk.Menu(self.master)
		self.filemenu = tk.Menu(self.menubar,tearoff=0)
		self.filemenu.add_command(label="Exit",command=self.ExitCommand)
		self.menubar.add_cascade(label="TnT2",menu=self.filemenu)

		#display menu
		self.master.config(menu=self.menubar)

	def ExitCommand(self):
		if tkMessageBox.askyesno("Quit","Are you sure?"):
			self.master.destroy()

class Editor(object):
	def __init__(self,master):
		self.master = master
		self.editor = tk.Frame(self.master)
		self.notelistframe = tk.Frame(self.master)

		self.text = tk.Text(self.editor,bg="white",height=8, width=4)
		self.text.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=1)

		self.scroll1v = tk.Scrollbar(self.notelistframe,orient=tk.VERTICAL)
		self.scroll2h = tk.Scrollbar(self.notelistframe,orient=tk.HORIZONTAL)
		self.notelist = tk.Listbox(self.notelistframe,bg="grey",yscrollcommand=self.scroll1v.set,selectmode=tk.EXTENDED)
		self.notelist = tk.Listbox(self.notelistframe,bg="grey",xscrollcommand=self.scroll2h.set,selectmode=tk.EXTENDED)
		self.scroll1v.configure(command=self.notelist.yview)
		self.scroll2h.configure(command=self.notelist.xview)
		self.scroll2h.pack(side=tk.BOTTOM,fill=tk.X)
		self.notelist.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
		self.scroll1v.pack(side=tk.RIGHT,fill=tk.Y)

		self.editor.pack(fill=tk.BOTH,side=tk.LEFT)
		self.notelistframe.pack(fill=tk.BOTH,expand=1,side=tk.RIGHT)
		self.buttons = Buttons(self.editor,self.text,self.notelist)
		self.text.bind("<Return>",self.return_insert)
		self.notelist.bind("<Double-Button-3>",self.delete_current)
		self.getNotes()

	def return_insert(self,event):
		self.buttons.enter()

	def delete_current(self,event):
		self.buttons.remove()

	def autoSave(self):
		self.buttons.save()
		self.master.after(60000 * 1, self.autoSave)

	def getNotes(self):
		try:
			f = file(notes_file, "rb")
			self.notes = pickle.load(f)
			for item in self.notes:
				self.notelist.insert(tk.END,xor_crypt(item,'d'))
			f.close()
		except:
			pass

class Buttons(object):
	def __init__(self,master,text,notes):
		self.master = master
		self.text = text
		self.notelist = notes
		self.enterButton = tk.Button(self.master,text="Enter",fg="green",font="bold",command=self.enter)
		self.removeButton = tk.Button(self.master,text="Remove",fg="green",font="bold",command=self.remove)
		self.saveButton = tk.Button(self.master,text="Save",fg="green",font="bold",command=self.save)
		self.showButtons()

	def enter(self):
		self.text_contents = self.text.get(1.0, tk.END)
		self.notelist.insert(tk.END, self.text_contents)
		self.text.delete(1.0,tk.END)

	def remove(self):
		self.notelist.delete(tk.ANCHOR)

	def save(self):
		f = file(notes_file, "wb")
		cip = []
		self.notes = self.notelist.get(0, tk.END)
		for n in self.notes:
			cip.append(xor_crypt(n,'e'))
		pickle.dump(cip, f)

	def showButtons(self):
		self.enterButton.pack(side=tk.LEFT)
		self.removeButton.pack(side=tk.LEFT)
		self.saveButton.pack(side=tk.LEFT)

if __name__ == '__main__':
	root = tk.Tk()
	myapp = MyApp(root)
