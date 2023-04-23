import tkinter as tk
from tkinter import ttk
from utils import *

class MainWindow(WindowInitialization):
    def __init__(self, is_root, width, heigth, title, bg, font, font_color, win_icon, alphabets_list):
        super().__init__(is_root, width, heigth, title, bg, font, font_color, win_icon)
        self.window.geometry("+10+10")
        # Encryption algorithm selection
        encryption_algorithm = ttk.Combobox(self.window,
                                            state='readonly', 
                                            values=[name[1].__doc__ for name in get_algorithms("encryption_functions")],
                                            width = 30)
        encryption_algorithm.set('Select Enctyption Algorithm')
        encryption_algorithm.grid(sticky='W', row=0,  column=0, padx=20, pady=10)
        selected_algorithm = encryption_algorithm.get
        
        # Alphabet selection
        alphabets = ttk.Combobox(self.window,
                                 state='readonly',
                                 values=[alphabet[1]for alphabet in alphabets_list],
                                 width=30)
        alphabets.set('Select Alphabet')
        alphabets.grid(sticky='W', row=1, column=0, padx=20, pady=10)
        selected_alphabet = alphabets.get

        # Action to perform section
        tk.Label(master=self.window, text="Action to perform:").grid(sticky='W',
                                                             row=2,
                                                             column=0,
                                                             padx=20,
                                                             pady=(10,0))        
        enc_rbtn_s = tk.StringVar(value="encrypt")
        enc_rbtn = ttk.Radiobutton(self.window, 
                                   text = 'Encrypt',
                                   style = 'Default.TRadiobutton',
                                   variable = enc_rbtn_s,
                                   value = "encrypt",
                                   command=lambda: self.rotate_labels(enc_rbtn_s, in_text_section.lbl, out_text_section.lbl))
        enc_rbtn.grid(sticky = 'W', row = 3, column = 0, padx = 40, pady = 5)
        denc_rbtn = ttk.Radiobutton(self.window,
                                    text = 'Decrypt',
                                    style = 'Default.TRadiobutton',
                                    variable = enc_rbtn_s,
                                    value = "decrypt",
                                    command = lambda: self.rotate_labels(enc_rbtn_s, in_text_section.lbl, out_text_section.lbl))
        denc_rbtn.grid(sticky = 'W', row = 4, column = 0, padx = 40, pady = 5)
        enc_rbtn_s.set("encrypt")

        # Text input section
        in_text_section = LabledFrame(self.window, "Enter the text to be encrypted:", TxtContainerY, None)
        in_text_section.grid(row = 5, column = 0, padx=20, pady=10)
        
        # Key input section
        self.key_section = LabledFrame(self.window, "Encryption key:", TxtContainerY, None)
        self.key_section.grid(row = 6, column = 0, padx = 20, pady = 10)
        
        # Out text section
        out_text_section = LabledFrame(self.window, "Encrypted text:", TxtContainerY, None)
        out_text_section.grid(row = 7, column = 0, padx = 20, pady = 10)
        
        # Button for encryption/decription
        btn = tk.Button(self.window, 
                        text = 'Encrypt text', 
                        bd = 1, 
                        bg = '#E0E0E0', 
                        fg = "black", 
                        width = 20, 
                        height = 2, 
                        relief = 'ridge')
        btn.bind('<Button-1>', lambda event: self.enc_button_action(event, 
                                                               alphabets_list, 
                                                               selected_alphabet, 
                                                               selected_algorithm, 
                                                               enc_rbtn_s, 
                                                               self.key_section.display_obj.txt,
                                                               in_text_section.display_obj.txt,
                                                               out_text_section.display_obj.txt))
        btn.grid(sticky = "w", row = 8, column = 0, padx = 20, pady = 20)


    def rotate_labels(self, rbtn_s, in_text_obj, out_text_obj):
        """Rotate text when a radiobutton was clicked (used in main window)"""
        if rbtn_s.get() == "encrypt":
            in_text_obj.config(text="Enter the text to be encrypted:")
            out_text_obj.config(text="Encrypted text:")
        elif rbtn_s.get() == "decrypt":
            in_text_obj.config(text="Enter the text to be decrypted:")
            out_text_obj.config(text="Decrypted text:")

    def enc_button_action(self, event, alphabets, selected_alphabet, selected_algorithm, rbtn_s, key, in_txt, out_txt):
        """Encryption button function"""
        alphabet_symbols = [alphabet[0] for alphabet in alphabets if alphabet[1] == selected_alphabet()]
        alphabet_symbols = ''.join(alphabet_symbols)
        for algorithm in get_algorithms("encryption_functions"):
            if selected_algorithm() == algorithm[1].__doc__:
                result = algorithm[1](in_txt.get('1.0', 'end-1c'),
                                    key.get('1.0', 'end-1c'), 
                                    rbtn_s.get(),
                                    alphabet_symbols)
                out_txt.delete("1.0",'end')
                out_txt.insert(tk.END, result)

    def start(self):
        """Start root window"""
        self.window.mainloop()


