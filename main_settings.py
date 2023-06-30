from PIL.Image import open
from PIL.ImageTk import PhotoImage
from tkinter import Tk

class MainWindow(Tk):
    def __init__(self : Tk, title : str,  width : int, height: int, minsize: int, path: str, dim: int):
        super().__init__()
        
        self.title(title)
        self.minsize( minsize, minsize )

        screen_width = self.winfo_screenwidth() # Width of the screen
      
        screen_height = self.winfo_screenheight() # Height of the screen
      
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % ( width, height, x, y))

        image = open(path).resize(( dim, dim ))
        icon = PhotoImage(image)
        
        self.iconphoto(True, icon)