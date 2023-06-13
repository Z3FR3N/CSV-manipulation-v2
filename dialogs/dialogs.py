from tkinter import ttk
from dialogs.window_setting import Window
from main_settings import MainWindow

# Error: calls a windows to display some sort of error

class Error(Window):
    def __init__(self, main_window: MainWindow, message : str):
        super().__init__(main_window,  'Errore', 200, 100)

        self.minsize(200, 150)
        
        self.focus()

        ttk.Label(  self,
                    text= message).pack(expand=True)
        
        self.grab_set()

# Parameters serves as taking input and initialize functions
        
class Parameters(Window):
    def __init__(self, main_window : MainWindow, width: int, height : int):
        super().__init__(main_window, 'Inserimento parametri', width, height)
        self.focus()
        self.grab_set()

class Loading(Window):
    def __init__(self, main_window: MainWindow, width: int, height: int):
        super().__init__(main_window, "Elaborazione in corso", width, height)

