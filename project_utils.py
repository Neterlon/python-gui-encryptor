import tkinter as tk
from inspect import getmembers, isfunction
import importlib


class TxtContainer:
    def __init__(self, parent_container, main_window):
        self.parent_container = parent_container
        self.main_window = main_window

    def create_txt_container(self, text_size=(70,6)):
        set_width, set_height = text_size
        txt_container = tk.Frame(self.parent_container, borderwidth=1, relief="sunken")
        self.txt = tk.Text(txt_container, width=set_width, height=set_height, wrap="none", borderwidth=0)
        txt_vsb = tk.Scrollbar(txt_container, orient="vertical", command=self.txt.yview)
        txt_hsb = tk.Scrollbar(txt_container, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=txt_vsb.set, xscrollcommand=txt_hsb.set)
        self.txt.grid(row=0, column=0, sticky="nsew")
        txt_vsb.grid(row=0, column=1, sticky="ns")
        txt_hsb.grid(row=1, column=0, sticky="ew")
        txt_container.grid_rowconfigure(0, weight=1)
        txt_container.grid_columnconfigure(0,weight=1)
        # Action to perform when buttons are clicked
        self.txt.bind("<Button-3>", self.copy_to_clipboard)
        return txt_container
    
    def copy_to_clipboard(self, event):
        output_text = self.txt.get('1.0', 'end-1c')
        self.parent_container.clipboard_clear()
        self.main_window.clipboard_append(output_text)
        self.main_window.clipboard_get()

def get_algorithms(algorithm_module):
    algorithm_module = importlib.import_module(algorithm_module)
    function_list = getmembers(algorithm_module, isfunction)
    return function_list
 
