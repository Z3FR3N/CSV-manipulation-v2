from dialogs.window_setting import Window
from tkinter import ttk

class Error(Window):
    # Taking a message to display an error
    def __init__(self, main_window, message : str):
        super().__init__(main_window, 'Errore', 200, 100)
        
        self.resizable(False, False) # it's not a huge window, doesn't need much space

        #Creating a main frame to place the content in
        main_err_frame = ttk.Frame(self, relief= 'flat', padding= 5)

        self.columnconfigure( 0, weight=1, pad= 5 )  # main_frame
        self.rowconfigure(  0, weight=1, pad= 5 )
        
        main_err_frame.grid(row= 0, column= 0, sticky='NSEW') # Frame ready

        # To center a Label we assing weight to row 0 and 2, they have a padding function
        for i in  [0, 2]:
          main_err_frame.rowconfigure(i, weight=2)
          main_err_frame.rowconfigure(i, weight=2)
        
        # We assign less weight to the row/column where the Label will sit in
        main_err_frame.rowconfigure(1, weight= 1)
        main_err_frame.columnconfigure(1, weight=1)

        err_text =ttk.Label(  main_err_frame,
                              text= message,
                              justify= 'center') # Creating the Label
        
        err_text.grid(row= 1, column= 1) # Placing the Label
        
# Parameters serves as taking input and initialize functions, usually is modified at will in functions_types
class Parameters(Window):
    # Takes input from the user to apply parameters for functions executions, it's resizable
    def __init__(self, main_window):
        super().__init__(main_window, 'Inserimento parametri', 300, 300)

class Loading(Window):
    # Tell the user to wait
    def __init__(self, main_window, width: int, height: int):
        super().__init__(main_window, "Elaborazione in corso", 200, 100)
        self.resizable(False, False) # it's not a huge window, doesn't need much space

