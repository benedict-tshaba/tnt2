#!/usr/bin/python


__version__ = "0.0.1"
__author__ = "Tshaba Phomolo Benedict"

import Tkinter as tk
import tkMessageBox
import pickle
import sched, time
from tnt2lib import xor_crypt

notes_file = "notes.db"

class Tnt2App(object):
	def __init__(self,master):
		self.master = master
		self.master.title("TNT2")
		self.master.geometry("600x400")
		editor = Editor(self.master)
		menubar = MenuBar(self.master)
		editor.autoSave()
		self.master.mainloop()

class MenuBar(object):
	def __init__(self,master):
		self.master = master
		menubar = tk.Menu(self.master)
		filemenu = tk.Menu(menubar,tearoff=0)
		filemenu.add_command(label="Exit",command=self.exit_command)
		menubar.add_cascade(label="TnT2",menu=filemenu)
		menubar.add_separator()
	
		editmenu = tk.Menu(menubar, tearoff=0)
		editmenu.add_command(label="Clear All", command=self.clear_command)
		editmenu.add_separator()
		editmenu.add_command(label="Prioritise", command=self.priori_command)
		menubar.add_cascade(label="Edit",menu=editmenu)

		helpmenu = tk.Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.about_command)
		menubar.add_cascade(label="Help", menu=helpmenu)

		#display menu
		self.master.config(menu=menubar)
	
	def about_command(self):
		pass

	def remove_command(self):
		pass

	def clear_command(self):
		pass	

	def priori_command(self):
		pass 

	def exit_command(self):
		if tkMessageBox.askyesno("Quit","Are you sure?"):
			self.master.destroy()

class Editor(object):
	def __init__(self,master):
		self.master = master
		editor = tk.Frame(self.master)
		notelistframe = tk.Frame(self.master)

		text = tk.Text(editor,bg="white",height=8, width=4)
		text.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=1)

		scroll1v = tk.Scrollbar(notelistframe,orient=tk.VERTICAL)
		scroll2h = tk.Scrollbar(notelistframe,orient=tk.HORIZONTAL)
		self.notelist = tk.Listbox(notelistframe,bg="grey",yscrollcommand=scroll1v.set,selectmode=tk.EXTENDED)
		self.notelist = tk.Listbox(notelistframe,bg="grey",xscrollcommand=scroll2h.set,selectmode=tk.EXTENDED)
		scroll1v.configure(command=self.notelist.yview)
		scroll2h.configure(command=self.notelist.xview)
		scroll2h.pack(side=tk.BOTTOM,fill=tk.X)
		self.notelist.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
		scroll1v.pack(side=tk.RIGHT,fill=tk.Y)

		editor.pack(fill=tk.BOTH,side=tk.LEFT)
		notelistframe.pack(fill=tk.BOTH,expand=1,side=tk.RIGHT)
		self.buttons = Buttons(editor,text,self.notelist)
		text.bind("<Return>",self.return_insert)
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
	myapp = Tnt2App(root)
