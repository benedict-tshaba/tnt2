#!/usr/bin/python

# Tnt2 is a re-write of my previous program Tnt. It is a simple note-taking
# program which I use to take class notes and write simple reminders.
# Copyright (C) 2017  Tshaba Phomolo Benedict

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


__version__ = "1.2.7"
__author__ = "Tshaba Phomolo Benedict"

import Tkinter as tk
import tkMessageBox
import pickle
import sched, time
from .tnt2lib import xor_crypt

notes_file = "notes.db"

class Tnt2App(object):
	def __init__(self,master):
		self.master = master
		self.master.title("TNT2")
		self.master.geometry("600x400")
		editor = Editor(self.master)
		menubar = MenuBar(self.master,editor)
		editor.autoSave()
		self.master.mainloop()

class MenuBar(object):
	def __init__(self,master,editor):
		self.master = master
		self.editor = editor
		menubar = tk.Menu(self.master)
		filemenu = tk.Menu(menubar,tearoff=0)
		filemenu.add_command(label="Exit",command=self.exit_command)
		menubar.add_cascade(label="TNT2",menu=filemenu)
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
		label = tkMessageBox.showinfo("About","Version: "+__version__+"\nTNT2 is a re-write of TNT using the OOP features of python. It is a simple note-taking application designed for ease of use. \nCreated by Tshaba Phomolo Benedict.")

	def clear_command(self):
		self.editor.notelist.delete(0,tk.END)	

	def priori_command(self):
		priori_text = self.editor.notelist.get(tk.ANCHOR)
 		self.editor.notelist.delete(tk.ANCHOR)
		self.editor.notelist.insert(0, priori_text)

	def exit_command(self):
		if tkMessageBox.askyesno("Quit","Are you sure?"):
			self.master.destroy()

class Editor(object):
	def __init__(self,master):
		self.master = master
		editor = tk.Frame(self.master)
		notelistframe = tk.Frame(self.master)

		self.text = tk.Text(editor,bg="white",height=8, width=4)
		self.text.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=1)

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
		self.buttons = Buttons(editor,self.text,self.notelist)
		self.text.bind("<Return>",self.return_insert)
		self.notelist.bind("<Double-Button-3>",self.delete_current)
		self.notelist.bind("<Double-Button-1>",self.copy_to_text)
		self.getNotes()

	def return_insert(self,event):
		self.buttons.enter()

	def copy_to_text(self,event):
		self.text.delete(1.0, tk.END)
		current_note = self.notelist.get(tk.ANCHOR)
		self.text.insert(1.0, current_note)

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
