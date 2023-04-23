import tkinter as tk
from tkinter import ttk
from utils import *

class PRNGWindow(WindowInitialization):
    def __init__(self, is_root, root_window, width, heigth, title, bg, font, font_color, win_icon):
        super().__init__(is_root, width, heigth, title, bg, font, font_color, win_icon)
        self.window.geometry("+780+10")
        # PRNG algorithm selection
        prng_algorithm = ttk.Combobox(self.window, 
                                      state = 'readonly',  
                                      values = [name[1].__doc__ for name in get_algorithms("prng_functions")], 
                                      width = 30)
        prng_algorithm.set('Select PRNG algorithm')
        prng_algorithm.grid(sticky='W', row=0,  column=0, padx=20, pady=10)
        selected_algorithm = prng_algorithm.get
        prng_algorithm.bind("<<ComboboxSelected>>", lambda event: self.prng_combobox_selection(event, selected_algorithm, instructions_text))

        # PRNG parameters input section
        in_param_text = LabledFrame(self.window, "Enter generator parameters: ", TxtContainerXY, (30, 10))
        in_param_text.grid(sticky = "nw", row = 1, column = 0, padx = 20, pady = 10)

        # PRNG instructions section
        instructions_frame = tk.Frame(self.window)
        instructions_frame.grid(sticky = "nw", row = 1, column = 1, pady = (29, 0))
        instructions_text = tk.Text(instructions_frame, 
                                    width = 60, 
                                    height = 7,
                                    wrap = "word",
                                    spacing1 = 10,
                                    spacing2 = 10,
                                    borderwidth = 0)
        instr_txt_vsb = tk.Scrollbar(instructions_frame, 
                                     orient="vertical", 
                                     command=instructions_text.yview)
        instructions_text.configure(yscrollcommand = instr_txt_vsb.set)
        instructions_text.grid(row=0, column=0, sticky="nsew")
        instr_txt_vsb.grid(row=0, column=1, sticky="ns")
        instructions_frame.grid_rowconfigure(0, weight=1)
        instructions_text.insert(tk.END, "Select a generator to get instructions")
        instructions_text.configure(state="disabled")

        # Output format section
        tk.Label(master=self.window, text="Output format:").grid(sticky = 'w',
                                                                 row = 2,
                                                                 column = 0,
                                                                 padx = 20,
                                                                 pady = (10, 0))        
        output_rbtn_s = tk.StringVar(value="dec")
        dec_output_rbtn = ttk.Radiobutton(self.window, 
                                   text = 'Decimal',
                                   style = 'Default.TRadiobutton',
                                   variable = output_rbtn_s,
                                   value = "dec")
        dec_output_rbtn.grid(sticky = 'W', row = 3, column = 0, padx = 40, pady = 5)
        bin_output_rbtn = ttk.Radiobutton(self.window,
                                    text = 'Binary',
                                    style = 'Default.TRadiobutton',
                                    variable = output_rbtn_s,
                                    value = "bin")
        bin_output_rbtn.grid(sticky = 'W', row = 4, column = 0, padx = 40, pady = 5)
        output_rbtn_s.set("dec")

        # Number of iterations section
        in_iter_num = LabledFrame(self.window, "Number of iterations: ", TxtContainerY, (20, 1))
        in_iter_num.grid(sticky = "nw", row = 2, column = 1, rowspan = 3, pady = 10)

        # Generation result section
        out_text_section = LabledFrame(self.window, "Generation result: ", TxtContainerY, (97, 10))
        out_text_section.grid(sticky = "w", row = 5, column = 0, padx = 20, pady = 10, columnspan = 2)

        # Button for sequence generation
        btn_gen = tk.Button(self.window, 
                        text = 'Generate sequence', 
                        bd = 1, 
                        bg = '#E0E0E0', 
                        fg = "black", 
                        width = 20, 
                        height = 2, 
                        relief = 'ridge')
        btn_gen.bind('<Button-1>', lambda event: self.prng_gen_button_action(event,
                                                                             selected_algorithm,
                                                                             in_param_text.display_obj.txt,
                                                                             in_iter_num.display_obj.txt,
                                                                             output_rbtn_s,
                                                                             out_text_section.display_obj.txt))
        btn_gen.grid(sticky = "w", row = 6, column = 0, padx = 20, pady = (20, 10))

        # Button to send the generated sequence as a key for a cipher
        btn_key_send = tk.Button(self.window, 
                        text = 'Send to key field', 
                        bd = 1, 
                        bg = '#E0E0E0', 
                        fg = "black", 
                        width = 20, 
                        height = 2, 
                        relief = 'ridge')
        btn_key_send.bind('<Button-1>', lambda event: self.prng_gen_button_action(event,
                                                                                  selected_algorithm,
                                                                                  in_param_text.display_obj.txt,
                                                                                  in_iter_num.display_obj.txt,
                                                                                  True,
                                                                                  root_window.key_section.display_obj.txt))
        btn_key_send.grid(sticky = "w", row = 7, column = 0, padx = 20, pady = (10, 20))


    def prng_combobox_selection(self, event, selected_algorithm, out_txt):
        """Actions performed when a combobox is selected"""
        for algoithm in get_algorithms("prng_functions"):
            if selected_algorithm() == algoithm[1].__doc__:
                result = algoithm[1](get_instructions = True)
                out_txt.configure(state="normal")
                out_txt.delete("1.0",'end')
                out_txt.insert(tk.END, result)
                out_txt.configure(state="disabled")

    def prng_gen_button_action(self, event, selected_algorithm, gen_prmt, iter_num, rbtn_s, out_txt):
        """Actions performed when buttons are clicked"""
        for algoithm in get_algorithms("prng_functions"):
            if selected_algorithm() == algoithm[1].__doc__:
                try:
                    if rbtn_s.get() == "dec":
                        gen_bin = False
                    else:
                        gen_bin = True
                except:
                    if rbtn_s == True:
                        gen_bin = True
                result = algoithm[1](gen_prmt.get('1.0', 'end-1c'),
                                    iter_num.get('1.0', 'end-1c'),
                                    gen_bin)
                out_txt.delete("1.0",'end')
                out_txt.insert(tk.END, result)