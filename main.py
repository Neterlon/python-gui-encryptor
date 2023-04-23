import settings
import utils
from mainWindow import *
from prngWindow import *

if __name__ == "__main__":
    # Main Window
    root = MainWindow(is_root = True,
                      width = settings.ROOT_WINDOW_WIDTH,
                      heigth = settings.ROOT_WINDOW_HEIGHT,
                      title = 'Symmetric encryptor',
                      bg = settings.BACKGROUND_COLOR,
                      font = settings.DEFAULT_FONT,
                      font_color = settings.FONT_COLOR,
                      win_icon = 'img/lock.png',
                      alphabets_list = settings.ALPHABETS)
    
    # Pseudorandom number generator window
    prng = PRNGWindow(is_root = False,
                      root_window = root,
                      width = settings.PRNG_WINDOW_WIDTH,
                      heigth = settings.PRNG_WINDOW_HEIGHT,
                      title = 'Pseudorandom number generator',
                      bg = settings.BACKGROUND_COLOR,
                      font = settings.DEFAULT_FONT,
                      font_color = settings.FONT_COLOR,
                      win_icon = 'img/random.png')
    
    root.start()
