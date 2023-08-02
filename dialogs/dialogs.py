from time import sleep
from numpy import column_stack
from dialogs.window_setting import Window
from general_settings import multicolumnconfigure, multirowconfigure
from tkinter.ttk import Frame, Label, Button, Separator, Progressbar
from tkinter import Scrollbar, Canvas, VERTICAL, NS, NSEW, NW, EW, NE, Toplevel

class Error(Window):
    # Taking a message to display an error
    def __init__(self, main_window, message : str):
        super().__init__(main_window, 'Errore', 200, 100)
        self.center()
        self.grab_set()
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
# TODO: adding a button to update the data list

class Parameters(Window):
    # Takes input from the user to apply parameters for functions executions, it's resizable
    def __init__(self, main_window, function):
        super().__init__(main_window, 'Inserimento parametri', 300, 300)

        self.right()
        self.resizable(False, False)
        self.title(function.name)
        self.focus()
        self.main_frame = Frame(self)

        # Creo i due sottoframe: il superiore ospita il contenuto, quello inferiore il bottone 'applica'
        self.content = Frame(self.main_frame)
        self.separator = Separator(self.main_frame, orient='horizontal')
        self.bottom_frame = Frame(self.main_frame)
        self.apply = Button(self.bottom_frame, text='Applica', command=function.generate) # ugly -> breaks encapsulation but i get circular import error
        self.update_data = Button(self.bottom_frame, text='Aggiorna', command=function.update_data)
        
        self.main_frame.grid_columnconfigure(0, weight=1, minsize= self.winfo_reqwidth())
        self.main_frame.grid_rowconfigure(0, weight=3, minsize= 260)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=2)
        self.main_frame.grid(column=0, row=0, sticky= NSEW)
        self.content.grid(column=0, row=0, sticky=NSEW)
        self.separator.grid(column=0, row=1, sticky=EW)
        self.bottom_frame.grid_columnconfigure(0, weight=2)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(2, weight=1)
        self.bottom_frame.grid_columnconfigure(3, weight=2)
        self.bottom_frame.grid(column=0, row=2, sticky=NSEW)
        # Bottone applica il comando predisposto
        self.apply.grid(column=1, row=0, pady=3)
        self.update_data.grid(column=2, row=0, pady=3)

class Loading(Window):
    # Tell the user to wait
    def __init__(self, main_window):
        super().__init__(main_window, "Elaborazione in corso", 200, 100)
        self.resizable(False, False) # it's not a huge window, doesn't need much space
        self.center()
        self.wm_withdraw()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0, sticky= NSEW)
        multicolumnconfigure(self.main_frame, [0,2], weight=1)
        multirowconfigure(self.main_frame,[0,1,2,3], weight=1)

        self.message = Label(self.main_frame, text='Attendere' )
        self.message.grid(row=1, column=1, pady=3)
        self.progressbar = Progressbar(self.main_frame, orient='horizontal', mode='indeterminate')
        self.progressbar.grid(column=1, row=2, sticky= EW)
        
    
    def start(self):
        self.wm_deiconify()
        self.grab_set()
        self.progressbar.start()
        
    def stop(self, message : str):
        self.progressbar.stop()
        self.message.config(text=message)
        sleep(2)
        self.destroy()

class ScrollableFrame(Frame):
    def __init__(self, parent, height, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.grid(column=1, row=0, sticky=NS)
        self.canvas = Canvas( self, bd=0, highlightthickness=0, 
                                height= height,
                                yscrollcommand=self.vscrollbar.set)
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        self.vscrollbar.config(command = self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,anchor=NW)
        self.interior.bind('<Enter>', self._bound_to_mousewheel)
        self.interior.bind('<Leave>', self._unbound_to_mousewheel)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
        
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
    
    def _bound_to_mousewheel(self, event):
      self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
      self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
      self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")