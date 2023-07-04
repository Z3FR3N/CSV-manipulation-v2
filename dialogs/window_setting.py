from main_settings import MainWindow
from tkinter import Toplevel

# abstract class that initialize a window object with useful parameters

class Window(Toplevel):
    def __init__(self, main_window : MainWindow, title: str, width: int, height: int):
        super().__init__(main_window, takefocus= True, width= width, height= height)

        self.transient(main_window)
        self.title(title)
        self.width = width
        self.height = height
        self.main_window = main_window
        self.main_window.update_idletasks()
        self.focus()
    
    def center(self):
      
      main_width = self.main_window.winfo_reqwidth() # Width of the main window
      main_x = self.main_window.winfo_x() # Main window x

      main_height = self.main_window.winfo_reqheight()# Height of the main window
      main_y = self.main_window.winfo_y() # Main window y

      # Calculate Starting X and Y coordinates for Window
      x = (main_x + (main_width / 2)) - (self.width / 2)
      y = (main_y + (main_height / 2)) - (self.height / 2)

      self.geometry('%dx%d+%d+%d' % ( self.width, self.height, x, y))
  
    def right(self):
      main_width = self.main_window.winfo_width() # Width of the main window
      main_x = self.main_window.winfo_x() # Main window x

      main_height = self.main_window.winfo_height()# Height of the main window
      main_y = self.main_window.winfo_y() # Main window y

      x = main_x + main_width + 5
      y = (main_y + (main_height / 2)) - (self.height / 2)

      self.geometry('%dx%d+%d+%d' % ( self.width, self.height, x, y))