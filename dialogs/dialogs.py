from tkinter import ttk
from dialogs.window_setting import Window, App

# Error: calls a windows to display some sort of error

class Error(Window):
    def __init__(self, main_window : App, message : str):
        super().__init__(main_window, 'Errore', 200, 100)
        
        err_frame = ttk.Frame(self, relief= 'flat', padding= 5)

        self.columnconfigure( 0, 
                              weight=1,
                              pad= 5 )  # self._main_frame
        
        self.rowconfigure(  0, 
                            weight=1,
                            pad= 5 )
        
        err_frame.grid(row= 0, column= 0, sticky='NSEW')

        for i in  [0, 2]:
          err_frame.rowconfigure(i, weight=2)
          err_frame.rowconfigure(i, weight=2)
          
        err_frame.rowconfigure(1, weight= 1)
        err_frame.columnconfigure(1, weight=1)

        err_text =ttk.Label(  err_frame,
                              text= message,
                              justify= 'center')
        
        err_text.grid(row= 1, column= 1)
        
# Parameters serves as taking input and initialize functions, usually is modified at will in functions_types

class Parameters(Window):
    def __init__(self, main_window : App, width : int, height : int):
        super().__init__(main_window, 'Inserimento parametri', width, height)
    # Conviene implementare due frame: uno superiore che contenga il contenuto vero e proprio e uno sottostante che contenga solo il bottone "applica" centrale

class Loading(Window):
    def __init__(self, main_window, width: int, height: int):
        super().__init__(main_window, "Elaborazione in corso", width, height)

