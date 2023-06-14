from tkinter import ttk
from dialogs.window_setting import Window
from main_settings import MainWindow

# Error: calls a windows to display some sort of error

class Error(Window):
    def __init__(self, main_window : MainWindow, message : str):
        super().__init__(main_window, 'Errore', 200, 100)

        self.minsize(200, 100)
        
        ttk.Label(  self,
                    text= message,
                    justify= 'center').pack(expand= True)
        
        self.focus()

# Parameters serves as taking input and initialize functions, usually is modified at will in functions_types

class Parameters(Window):
    def __init__(self,main_window : MainWindow, width: int, height : int):
        super().__init__(main_window, 'Inserimento parametri', width, height)

        self._par_frame = ttk.Frame(  self, 
                                      relief='flat')
        
        self._par_frame.grid(   column=0, 
                                row=0, 
                                sticky=('NSEW') )
        
    @property
    def par_frame(self):
      return self._par_frame

class Loading(Window):
    def __init__(self, main_window : MainWindow, width: int, height: int):
        super().__init__(main_window, "Elaborazione in corso", width, height)

