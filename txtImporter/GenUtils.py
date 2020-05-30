#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import re
import tkinter.ttk as tkinter_ttk	#Essential for ttk. commands

def centerWindow(win):
	"""
	This function centres the window that is passed to it as the parameter.
	Always set up the widgets in the window to be centred before calling this function
	Does not take the size of the title bar or any menus into consideration
	"""
	win.update_idletasks()  # Update "requested size" from geometry manager
	xpos = (win.winfo_screenwidth() - win.winfo_reqwidth()) / 2
	ypos = (win.winfo_screenheight() - win.winfo_reqheight()) / 2	
	win.geometry("+%d+%d" % (xpos, ypos))
	win.deiconify()
	