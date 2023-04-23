import tkinter as tk
from inspect import getmembers, isfunction
import importlib
from tkinter import ttk
import subprocess 

class WindowInitialization:
    """Сlass designed to create a window and define its main settings"""
    def __init__(self, is_root, width, heigth, title, bg, font, font_color, win_icon):
        # Window initialization
        if is_root == True:
            self.window = tk.Tk()
        else: self.window = tk.Toplevel()
        # Window properties
        self.window.minsize(width=width, 
                            height=heigth)
        self.window.title(title)
        self.window_icon = tk.PhotoImage(file=win_icon)
        self.window.iconphoto(False, self.window_icon)
        # General application style   
        self.window.configure(bg=bg)
        self.window.option_add("*Font", font)
        self.window.option_add("*foreground", font_color)
        self.window.option_add("*background", bg)
        self.window.option_add('*TCombobox*Listbox*Background', 'white')
        self.window.option_add('*TCombobox*Listbox*Foreground', 'RoyalBlue4')
        # Radiobutton style
        rbtn_style = ttk.Style()
        rbtn_style.configure('Default.TRadiobutton',
                             background=bg,
                             font=font,
                             foreground=font_color)
    
class LabledFrame(tk.Frame):
    """Create a frame that contains label and passed object"""
    def __init__(self, master, lbl_text, display_obj, display_obj_prmt):
        tk.Frame.__init__(self, master)
        self.lbl = tk.Label(master=self, 
                            text=lbl_text)
        self.display_obj = display_obj(self, display_obj_prmt)
        self.lbl.grid(row = 0, 
                      column = 0, 
                      sticky="W",
                      pady=(0, 7))
        self.display_obj.grid(row = 1, column = 0)

class TxtContainerY(tk.Frame):
    """Textbox with vertial scroll"""
    def __init__(self, master, textbox_size=(70,4)):
        tk.Frame.__init__(self, master)
        if textbox_size == None:
            textbox_size = (70,4)
        width, height = textbox_size
        self.txt = tk.Text(self, 
                           width=width, 
                           height=height, 
                           wrap="word", 
                           borderwidth=0,
                           bg="white",
                           foreground="black")
        self.txt_vsb = tk.Scrollbar(self, 
                                    orient="vertical", 
                                    command=self.txt.yview)
        self.txt.configure(yscrollcommand=self.txt_vsb.set)
        self.txt.grid(row=0, column=0, sticky="nsew")
        self.txt_vsb.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.txt.bind("<Button-3>", self.copy_to_clipboard)
    def copy_to_clipboard(self, event):
        output_text = self.txt.get('1.0', 'end-1c')
        subprocess.run("clip", text=True, input=output_text)

class TxtContainerXY(tk.Frame):
    """Textbox with vertical and horizontal scroll"""
    def __init__(self, master, textbox_size=(70,6)):
        tk.Frame.__init__(self, master)
        if textbox_size == None:
            textbox_size = (70,4)
        width, height = textbox_size
        self.txt = tk.Text(self, 
                           width = width, 
                           height = height, 
                           wrap = "none", 
                           borderwidth = 0,
                           bg = "white",
                           foreground = "black")
        self.txt_vsb = tk.Scrollbar(self, 
                                    orient = "vertical", 
                                    command = self.txt.yview)
        self.txt_hsb = tk.Scrollbar(self, 
                                    orient = "horizontal", 
                                    command = self.txt.xview)
        self.txt.configure(yscrollcommand = self.txt_vsb.set, 
                           xscrollcommand = self.txt_hsb.set)
        self.txt.grid(row = 0, column = 0, sticky = "nsew")
        self.txt_vsb.grid(row = 0, column = 1, sticky = "ns")
        self.txt_hsb.grid(row = 1, column = 0, sticky = "ew")
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.txt.bind("<Button-3>", self.copy_to_clipboard)
    def copy_to_clipboard(self, event):
        output_text = self.txt.get('1.0', 'end-1c')
        subprocess.run("clip", text=True, input=output_text)

def get_algorithms(algorithm_module):
    """Get functions that exist in a module"""
    algorithm_module = importlib.import_module(algorithm_module)
    function_list = getmembers(algorithm_module, isfunction)
    return function_list