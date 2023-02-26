import tkinter as tk
from tkinter import ttk
import settings
import project_utils
from enctyption_gui import EncGui

if __name__ == "__main__":
    #
    # Window configuration
    #
    root = tk.Tk()
    root.minsize(width=settings.WINDOW_MIN_WIDTH, height=settings.WINDOW_MIN_HEIGHT)
    root.geometry("+10+10")
    root.option_add("*Font", settings.DEFAULT_FONT)
    root.title('Symmetric encryptor')
    window_icon = tk.PhotoImage(file='img/lock.png')
    root.iconphoto(True, window_icon)

    #
    #  Main Frame
    #
    main_frame = tk.Frame(root, bg=settings.BACKGROUND_COLOR, padx=40, pady=40)
    main_frame.pack(side=tk.TOP, fill=tk.X)

    # Get the names of encryption algorithms from the module specified in the get_algorithms function
    encryption_algorithm_list = project_utils.get_algorithms('encryption_functions')

    # Сreate a section containing graphic elements
    enc_section = EncGui(encryption_algorithm_list, settings.ALPHABETS, 'settings', root)
    enc_section.create_gui_section(main_frame)


    root.mainloop()