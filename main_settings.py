from PIL import Image, ImageTk
import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self : tk.Tk, title : str,  width : int, height: int, minsize: int, path: str, dim: int):
        super().__init__()
        
        self.title(title)
        self.minsize( minsize, minsize )

        # Width of the screen
        screen_width = self.winfo_screenwidth()
        # Height of the screen
        screen_height = self.winfo_screenheight()
        
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % ( width, height, x, y))
    
        image = Image.open(path).resize(( dim, dim ))
        icon = ImageTk.PhotoImage(image)
        
        self.iconphoto(True, icon)
