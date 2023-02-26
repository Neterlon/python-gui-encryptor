import tkinter as tk
from tkinter import ttk
import project_utils
import importlib


class EncGui:
    def __init__(self, encryption_algorithms, alphabets, settings_module, main_window):
        self.encryption_algorithms = encryption_algorithms
        self.alphabets = alphabets
        self.settings = importlib.import_module(settings_module)
        self.main_window = main_window
        self.in_text = None
        self.enc_key = None
        self.out_text = None

    # Combobox with allowed encryption_algorithms
    def create_algorithm_combobox(self, parent_container):
        encryption_algorithm_frame = tk.Frame(parent_container)
        encryption_algorithm_frame.pack(side=tk.TOP, 
                             anchor=tk.W,
                             pady=(20,0))
        encryption_algorithm_names = [name[1].__doc__ for name in self.encryption_algorithms]
        encryption_algorithm = ttk.Combobox(encryption_algorithm_frame, 
                                            state='readonly', 
                                            values=encryption_algorithm_names,
                                            width = 25)
        encryption_algorithm.set('Select Enctyption Algorithm')
        encryption_algorithm.grid(sticky='W', 
                                  row=0, 
                                  column=0)
        self.selected_algorithm = encryption_algorithm.get

    def create_alphabet_combobox(self, parent_container):
        alphabet_frame = tk.Frame(parent_container)
        alphabet_frame.pack(side=tk.TOP, 
                             anchor=tk.W,
                             pady=(20,0))
        alphabets = ttk.Combobox(alphabet_frame,
                                 state='readonly',
                                 values=[alphabet[1]for alphabet in self.alphabets],
                                 width=25)
        alphabets.set('Select Alphabet')
        alphabets.grid(sticky='W',
                       row=0,
                       column=0)
        self.selected_alphabet = alphabets.get
        
    # Radiobutton that decides what action to perform (encryption or decryption)
    def create_radiobutton(self, parent_container):
        # Radiobutton style
        rbtn_style = ttk.Style()
        rbtn_style.configure('Default.TRadiobutton',
                             background=parent_container['bg'],
                             foreground=self.settings.FONT_COLOR,
                             font=self.settings.DEFAULT_FONT)
        # Radiobutton Frame
        radiobutton_frame = tk.Frame(parent_container, bg=parent_container['bg'])
        radiobutton_frame.pack(side=tk.TOP, 
                             anchor=tk.W,
                             pady=(20,0))
        # Label to the radiobuttons
        rbtn_lbl = tk.Label(radiobutton_frame, 
                            text='Action to Perform:',
                            bg=parent_container['bg'],
                            fg=self.settings.FONT_COLOR)
        # Radiobuttons 
        self.rbtn_s = tk.StringVar(value="encrypt")
        enc_rbtn = ttk.Radiobutton(radiobutton_frame, 
                                   text='Encrypt',
                                   style='Default.TRadiobutton',
                                   variable=self.rbtn_s,
                                   value="encrypt",
                                   command=self.rotate_labels)
        denc_rbtn = ttk.Radiobutton(radiobutton_frame,
                                    text='Decrypt',
                                    style='Default.TRadiobutton',
                                    variable=self.rbtn_s,
                                    value="decrypt",
                                    command=self.rotate_labels)
        rbtn_lbl.pack()
        enc_rbtn.pack()
        denc_rbtn.pack()
        
    # Create a box into which text is entered
    def create_in_textbox(self, parent_container, main_window, textbox_size=(70,6)):
        in_text_frame = tk.Frame(parent_container, bg=parent_container['bg'])
        in_text_frame.pack(side=tk.TOP, 
                             anchor=tk.W, 
                             pady=(20,0))
        # Label to the text container with plain text
        self.in_text_lbl = tk.Label(in_text_frame, 
                               text='Enter the text to be encrypted:', 
                               bg=parent_container['bg'], 
                               fg=self.settings.FONT_COLOR)
        self.in_text_lbl.grid(sticky='W', 
                         row=0, 
                         column=0)
        # Text Container (Plain Text to be encrypted)
        in_text = project_utils.TxtContainer(in_text_frame, main_window)
        in_text.create_txt_container(textbox_size).grid(sticky='W',
                                                   row=1, 
                                                   column=0, 
                                                   pady=(10,0))
        self.in_text = in_text

    # Create a box with information about encryption key
    def create_key_textbox(self, parent_container, main_window, textbox_size=(70,1)):
        keytext_frame = tk.Frame(parent_container, bg=parent_container['bg'])
        keytext_frame.pack(side=tk.TOP, 
                             anchor=tk.W,
                             pady=(20,0))
        # Label to the text container with encryption key
        enc_key_lbl = tk.Label(keytext_frame, 
                               text='Encryption Key:', 
                               bg=parent_container['bg'], 
                               fg=self.settings.FONT_COLOR)
        enc_key_lbl.grid(sticky='W', 
                         row=0, 
                         column=0)
        # Text Container (Encryption Key)
        enc_key = project_utils.TxtContainer(keytext_frame, main_window)
        enc_key.create_txt_container(textbox_size).grid(sticky='W',
                                                row=1, 
                                                column=0, 
                                                pady=(10,0))
        self.enc_key = enc_key

    # Create a box with information about encrypted text
    def create_out_textbox(self, parent_container, main_window, textbox_size=(70,6)):
        out_text_frame = tk.Frame(parent_container, bg=parent_container['bg'])
        out_text_frame.pack(side=tk.TOP, 
                             anchor=tk.W,
                             pady=(20,0))
        # Label to the text container with encrypted text
        self.out_text_lbl = tk.Label(out_text_frame, 
                               text='Encrypted Text:', 
                               bg=parent_container['bg'], 
                               fg=self.settings.FONT_COLOR)
        self.out_text_lbl.grid(sticky='W', 
                         row=0, 
                         column=0)
        # Text Container (Encrypted text)
        out_text = project_utils.TxtContainer(out_text_frame, main_window)
        out_text.create_txt_container(textbox_size).grid(sticky='W',
                                                  row=1, 
                                                  column=0, 
                                                  pady=(10,0))
        # Output Text
        self.out_text = out_text.txt
        

    def create_button(self, parent_container):
        btn_frame = tk.Frame(parent_container, bg=parent_container['bg'])
        btn_frame.pack(side=tk.TOP, 
                       anchor=tk.W,
                       pady=(20,0))
        btn = tk.Button(btn_frame, text='Encrypt text', bd=1, bg='#E0E0E0', width=20, height=2, relief='ridge')
        btn.bind('<Button-1>', self.button_action)
        btn.grid(row=0,column=0)

    def button_action(self, event):
        alphabet_symbols = [alphabet[0] for alphabet in self.settings.ALPHABETS if alphabet[1] == self.selected_alphabet()]
        alphabet_symbols = ''.join(alphabet_symbols)
        for algorithm in self.encryption_algorithms:
            if self.selected_algorithm() == algorithm[1].__doc__:
                result = algorithm[1](self.in_text.txt.get('1.0', 'end-1c'),
                                      self.enc_key.txt.get('1.0', 'end-1c'), 
                                      self.rbtn_s.get(),
                                      alphabet_symbols)
                self.out_text.delete("1.0",'end')
                self.out_text.insert(tk.END, result)

    def rotate_labels(self):
        if self.rbtn_s.get() == "encrypt":
            self.in_text_lbl.config(text="Enter the text to be encrypted:")
            self.out_text_lbl.config(text="Encrypted Text:")
        elif self.rbtn_s.get() == "decrypt":
            self.in_text_lbl.config(text="Enter the text to be decrypted:")
            self.out_text_lbl.config(text="Decrypted Text:")


    # Automatically create all GUI elements using one method
    def create_gui_section(self, parent_container):
        self.create_algorithm_combobox(parent_container)
        self.create_alphabet_combobox(parent_container)
        self.create_radiobutton(parent_container)
        self.create_in_textbox(parent_container, self.main_window)
        self.create_key_textbox(parent_container, self.main_window)
        self.create_out_textbox(parent_container, self.main_window)
        self.create_button(parent_container)
