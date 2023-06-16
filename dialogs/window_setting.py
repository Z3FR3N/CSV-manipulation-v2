import tkinter as tk
from main import App

# abstract class that initialize a window object with useful parameters

class Window(tk.Toplevel):
    def __init__(self, main_window : App, title: str, width: int, height: int):
        super().__init__(main_window, takefocus= True, width= width, height= height)

        self.transient(main_window)
        self.title(title)
        self.minsize(100, 100)

        # Width of the main window
        screen_width = self.winfo_screenwidth()
        # Height of the main window
        screen_height = self.winfo_screenheight()
        
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % ( width, height, x, y))

        self.resizable(False,False)
        self.grab_set()
        self.lift()