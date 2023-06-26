from dialogs.window_setting import Window, MainWindow
from tkinter.ttk import Frame, Label, Button, Separator
from tkinter import Scrollbar, Canvas

class Error(Window):
    # Taking a message to display an error
    def __init__(self, main_window : MainWindow, message : str):
        super().__init__(main_window, 'Errore', 200, 100)
        
        self.resizable(False, False) # it's not a huge window, doesn't need much space

        #Creating a main frame to place the content in
        main_err_frame = Frame(self, relief= 'flat', padding= 5)

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

        err_text = Label( main_err_frame,
                          text= message,
                          justify= 'center') # Creating the Label
        
        err_text.grid(row= 1, column= 1) # Placing the Label
        
# Parameters serves as taking input and initialize functions, usually is modified at will in functions_types
class Parameters(Window):
    # Takes input from the user to apply parameters for functions executions, it's resizable
    def __init__(self, main_window : MainWindow, function):
        super().__init__(main_window, 'Inserimento parametri', 300, 310)

        self.resizable(False, False)
        self.title(function.name)
        self.grid_columnconfigure(0, minsize=300)
        self.grid_rowconfigure(0, minsize=300)

        main_frame = Frame(self)
        main_frame.grid(column=0, row=0)
        main_frame.grid_columnconfigure(0, minsize=300, weight=1)
        main_frame.grid_rowconfigure(0, minsize=275, weight=3)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=2)

        # Creo i due sottoframe: il superiore ospita il contenuto, quello inferiore il bottone 'applica'
        self._content =  Frame(main_frame)
        self._content.grid(column=0, row=0, sticky='NSEW')
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(0, weight=1)
        
        separator = Separator(main_frame, orient='horizontal')
        separator.grid(column=0, row=1, sticky='EW')

        bottom_frame = Frame(main_frame)
        bottom_frame.grid(column=0, row=2, sticky='NSEW')
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        # Bottone applica il comando predisposto
        apply = Button(bottom_frame, text=('Applica \"' + function.name + '\"'), command=function.generate) # ugly, i agree. But breaks encapsulation but i get circular import error
        apply.grid(column=1, row=0, pady=5)
        

        ## Creo un Canvas per il top_frame -> CANVAS NON RILEVA CORRETTAMENTE LE DIMENSIONI
        #self.canvas = Canvas(top_frame, width=(278), highlightthickness=0)
        #self.canvas.pack(side= 'left', fill='both', expand=1)
        #self.canvas.grid_propagate(False)
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
#
        ## Creo una scrollbar per il Canvas
        #scrollbar = Scrollbar(top_frame, orient= 'vertical', command= self.canvas.yview)
        #scrollbar.pack(side='right', fill='y')
#
        ## Configuro il Canvas
        #self.canvas.configure(yscrollcommand=scrollbar.set)
        #self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
        ## Creo un frame interno al Canvas
        #self._content = Frame(self.canvas)
        #self._content.rowconfigure(0, weight=2)
        #self._content.columnconfigure(0, weight=2)
#
        ## Aggiungo contenuto all'interno di una finestra del canvas
        #self.canvas.create_window((0,0), window=self._content, anchor='nw')
        
        
    
    @property
    def content(self):
      return self._content

    #def _on_mousewheel(self, event):
    #  self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class Loading(Window):
    # Tell the user to wait
    def __init__(self, main_window, width: int, height: int):
        super().__init__(main_window, "Elaborazione in corso", 200, 100)
        self.resizable(False, False) # it's not a huge window, doesn't need much space