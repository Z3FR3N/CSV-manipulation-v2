from main_settings import *
from dialogs.dialogs import *
from functions.functions import *
import functions
import pandas as pd
# import customtkinter as ctk -> can be useful for restyling
from tkinter import filedialog as fd
from pandastable import Table # plotting a table from a DataFrame
import inspect # elaborating to what to do
import sys # elaborating to what to do

""" 
TODO: - Code optimization through Loop and better Attributes assignment
      - Creare un attributo di tipo lista con oppurtuni setter e getter per 
      - Better encapsulate elements
      - Differenziare il caricamento del primo e del secondo file con bottoni appositi [v]
      - Label for Comboboxes [v]
      - Completare la lettura del dataframe [v]
      - Cominciare l'implementazione delle funzioni
"""

class App(MainWindow):
    
    def __init__(self):
        super().__init__('Manipolazione CSV', 550, 500, 400, "CSV manipulation v2\\ICO.png", 30 )

        self._first_file_name = tk.StringVar(value= 'Nessun File caricato.')
        self._second_file_name = tk.StringVar(value= 'Nessun File caricato.')
        self._first_sep = tk.StringVar()
        self._second_sep = tk.StringVar()
        self._selected_function = tk.StringVar()
        self._functions_list = self.create_list()
        self._first_loaded_file = None
        self._second_loaded_file = None

        # Adding interface's elements, most complex ones with dedicated method
        self.create_widgets()

        # Initially, preview will be empty
        self.reset() 
        
        # Always create the grid AFTER widgets
        self.create_grid()
    
    # Using property to make accessible read-only values
    
    @property
    def first_file(self):
        return self._first_loaded_file
    
    @property
    def first_separator(self):
        return self._first_sep
    
    @property
    def second_separator(self):
        return self._second_sep
    
    @property
    def second_file(self):
        return self._second_loaded_file

    # METHODS

    def create_widgets(self):

        self._main_frame = ttk.Frame( self, 
                                      relief='flat')

        # Buttons of the main view

        self._reset = ttk.Button( self._main_frame,
                                  text='Reset',
                                  command= self.reset)
        
        self._inverti = ttk.Button( self._main_frame,
                                    text='Inverti',
                                    command= self.switch)
        
        self._carica = ttk.Button(  self._main_frame,
                                    text='Carica CSV',
                                    command= self.load)
        
        self._salva = ttk.Button( self._main_frame,
                                  text= 'Salva',
                                  command = self.save,
                                  state=tk.DISABLED)
        
        self._info = ttk.Button(  self._main_frame,
                                  text= 'Info',
                                  command= self.info)
        
        self._genera = ttk.Button(  self._main_frame,
                                    text= 'Genera',
                                    command= self.generate)
                
        # Combobox for selecting the function to launch

        # Identify the right function

        self._functions_frame = ttk.Frame(self._main_frame)
        
        self._functions_text = ttk.Label( self._functions_frame,
                                          text= "Lista funzioni: ",
                                          justify= 'left',
                                          anchor='center')

        self._functions_cbox = ttk.Combobox(  self._functions_frame, 
                                              textvariable= self._selected_function,
                                              # values: lists of functions available
                                              values= self._functions_list)
        
        self._functions_text.grid(row= 0, column= 0)
        self._functions_cbox.grid(row= 0, column= 1, sticky=('WE'))

        self._functions_frame.rowconfigure(0, weight=1)
        self._functions_frame.columnconfigure(0, weight= 1)
        self._functions_frame.columnconfigure(1, weight=2)

        # Due sezioni con LabelFrame da riempire con il nome dei file caricati
        
        self._first_name = tk.LabelFrame(   self._main_frame, 
                                            text= 'CSV 1',
                                            labelanchor='n',
                                            relief= 'groove')
        
        self._display_name1 = ttk.Label(  self._first_name, 
                                          textvariable= self._first_file_name,
                                          justify= 'center',
                                          anchor='center',
                                          padding= 3)
        
        self._second_name = tk.LabelFrame(  self._main_frame, 
                                            text='CSV 2',
                                            labelanchor='n',
                                            relief= 'groove')
        
        self._display_name2 = ttk.Label(  self._second_name, 
                                          textvariable= self._second_file_name,
                                          justify= 'center',
                                          anchor='center',
                                          padding= 3)

        self._sep_text1 = ttk.Label(  self._first_name, 
                                      text= 'Separatore:')
        
        self._sep_text2 = ttk.Label(  self._second_name, 
                                      text= 'Separatore:')
        
        self._first_sep_dotcomma = ttk.Radiobutton( self._first_name,
                                                    text=';',
                                                    variable= self._first_sep,
                                                    value= ';')
        
        self._load_first = ttk.Button(  self._first_name,
                                        text= 'Carica CSV 1',
                                        command= self.load_first)
        
        self._load_second = ttk.Button( self._second_name,
                                        text= 'Carica CSV 2',
                                        command= self.load_second)
        
        # setting default separator
        self._first_sep_dotcomma.invoke()
        
        self._first_sep_comma = ttk.Radiobutton(  self._first_name,
                                                  text=',',
                                                  variable= self._first_sep,
                                                  value= ',')
                
        self._second_sep_dotcomma = ttk.Radiobutton(  self._second_name,
                                                      text=';',
                                                      variable= self._second_sep,
                                                      value= ';')
        
        self._second_sep_comma = ttk.Radiobutton(   self._second_name,
                                                    text=',',
                                                    variable= self._second_sep,
                                                    value= ',')
        
        # setting default separator
        self._second_sep_dotcomma.invoke()
        
        # Notebook for preview

        self._csv_preview = ttk.Notebook( self._main_frame) 
                                          #width= self. - 20, 
                                          #height= self.height - 150)

    def create_grid(self):
        
        self._main_frame.grid(  column=0, 
                                row=0, 
                                sticky=('NSEW') )
        
        # Row 1

        self._functions_frame.grid(  column= 1,
                                    row= 0,
                                    columnspan= 2,
                                    sticky=('EW'),
                                    pady= 5 )

        self._info.grid(  column= 0,
                          row= 0,
                          pady= 5  )

        self._genera.grid(  column= 3,
                            row= 0,
                            pady= 5  )
        
        # Row 2

        self._csv_preview.grid( column= 0,
                                row= 1,
                                columnspan= 4,
                                pady= 5,
                                padx= 2,
                                sticky=('NSEW') )
        
        # Row 3
        
        # Placing objects inside the first Labelframe

        self._sep_text1.grid( column= 0,
                              row= 1,
                              sticky= 'E' )
        
        self._first_sep_dotcomma.grid(  row= 1, 
                                        column= 1 )
        
        self._first_sep_comma.grid( row= 1,
                                    column= 2,
                                    sticky= 'W')
        
        self._display_name1.grid( row= 0, 
                                  column= 0,
                                  columnspan= 3)
        
        self._load_first.grid(  column= 0,
                                row= 2,
                                sticky=('NSEW'),
                                columnspan= 3)
        
        # LabelFrame ready
        
        self._first_name.grid(  column= 0,
                                row= 2,
                                columnspan= 2,
                                sticky=('EW'),
                                padx= 5,
                                pady= 5 )
        
        # Placing objects inside the second Labelframe
        
        self._sep_text2.grid(   column= 0,
                                row= 1,
                                sticky= 'E' )
        
        self._second_sep_dotcomma.grid(   row= 1, 
                                          column= 1 )
        
        self._second_sep_comma.grid(  row= 1,
                                      column= 2,
                                      sticky= 'W')
        
        self._load_second.grid( column= 0,
                                row= 2,
                                sticky=('NSEW'),
                                columnspan= 3)
        
        self._display_name2.grid( row= 0,
                                  column= 0, 
                                  columnspan= 3)
        
        # LabelFrame ready
        
        self._second_name.grid( column= 2,
                                row= 2,
                                columnspan= 2,
                                sticky= ('EW'),
                                padx= 5,
                                pady= 5)
        
        # Configure rows and columns to display the labelframe
        
        self._first_name.rowconfigure(  0, 
                                        weight= 1,
                                        pad=2)
        
        self._first_name.rowconfigure(  1,
                                        weight= 1,
                                        pad=2)

        self._first_name.rowconfigure(  2,
                                        weight= 1,
                                        pad=2)

        self._first_name.columnconfigure( 0,
                                          weight= 1)

        self._first_name.columnconfigure( 1,
                                          weight= 1)

        self._first_name.columnconfigure( 2,
                                          weight= 1)

        self._second_name.rowconfigure( 0,
                                        weight= 1,
                                        pad=2)
        
        self._second_name.rowconfigure( 1,
                                        weight= 1,
                                        pad=2)
        
        self._second_name.rowconfigure( 2,
                                        weight= 1,
                                        pad=2)
        
        self._second_name.columnconfigure(  0,
                                            weight= 1)
        
        self._second_name.columnconfigure(  1,
                                            weight= 1)
        
        self._second_name.columnconfigure(  2,
                                            weight= 1)

        # Row 4

        self._reset.grid( column= 0, 
                          row= 3,
                          pady= 5)

        self._inverti.grid(   column= 1,
                              row= 3,
                              pady= 5 )

        self._carica.grid(  column= 2,
                            row= 3,
                            pady= 5 )

        self._salva.grid(   column= 3,
                            row= 3,
                            pady= 5)

        # weights for resizing and to initialize spacing

        self.columnconfigure( 0, 
                              weight=1,
                              pad= 5)  # self._main_frame
        
        self.rowconfigure(  0, 
                            weight=1,
                            pad= 5)     # self._main_frame
        
        self._main_frame.columnconfigure( 0, 
                                          weight=1,
                                          pad= 3)

        self._main_frame.columnconfigure( 1, 
                                          weight=3,
                                          pad= 3)
        
        self._main_frame.columnconfigure( 2, 
                                          weight=3,
                                          pad= 3) 
        
        self._main_frame.columnconfigure( 3, 
                                          weight=1,
                                          pad= 3)
        
        self._main_frame.rowconfigure(  1,
                                        weight= 5)      

    def clean_preview(self, count = 0):
      for i in self._csv_preview.tabs():
          self._csv_preview.forget(i)

      # No Preview
      self._no_preview = ttk.Frame( self._csv_preview)
      self._no_preview_loaded = ttk.Label(  self._no_preview, 
                                            text='Nessun file caricato')
      
      self._no_preview_loaded.place(  relx=0.5, 
                                      rely=0.5, 
                                      anchor=tk.CENTER)
      
      self._csv_preview.add(self._no_preview, text= 'No csv')
      
      if (len(self._csv_preview.tabs()) > 1 and count <= len(self._csv_preview.tabs())):
         self._csv_preview.forget(count)

    def draw_preview(self, data : pd.DataFrame, name: str, position: int):

      # DataFrame loaded
      self._csv = ttk.Frame(  self._csv_preview,
                              relief= 'flat')   
      
      # Populating the frames
      self._table = Table(  self._csv, 
                            dataframe= data,
                            showtoolbar= False, 
                            showstatusbar= False,
                            editable = False,
                            enable_menus= False )
      self._table.show()

      if (len(self._csv_preview.tabs()) > position):

        self._csv_preview.insert( position, 
                                  self._csv, 
                                  text = name )
        self._csv_preview.select(self._csv)

      else:
        self._csv_preview.add( self._csv, text= name)  
        self._csv_preview.select(self._csv)
      
      if (len(self._csv_preview.tabs()) >= 3 ):
        self._carica.config(state=tk.DISABLED)
      
    def switch(self):
        
        if((self._first_loaded_file != None and self._second_loaded_file) != None and len(self._csv_preview.tabs()) > 2):

          tmp = self._first_loaded_file
          self._first_loaded_file = self._second_loaded_file
          self._second_loaded_file = tmp

          tmp = tk.StringVar()
          tmp.set(self._first_file_name.get())
          self._first_file_name.set(self._second_file_name.get())
          self._second_file_name.set(tmp.get())

          tmp = self._csv_preview.tabs()[2]
          self._csv_preview.insert(1, tmp)
          self._csv_preview.select(1)
          
        else:
           
           Error(self, "Carica i due CSV!")
           #window.grab_set

    def info(self):
      ColumnsComparison(self)
      print(dir(ColumnsComparison))

    def reset(self, count = 0):
        
        if (count == 0):
          self._first_loaded_file = None
          self._second_loaded_file = None

          self._first_file_name.set('Nessun File caricato.')
          self._second_file_name.set('Nessun File caricato.')

          self.clean_preview()
          self._carica.config(state= tk.ACTIVE)

        if (count == 1):
           self._first_loaded_file = None
           self._first_file_name.set('')
           self.clean_preview()

        if (count == 2):
           self._second_loaded_file = None
           self._second_file_name.set('')
           self.clean_preview(count)

    def generate(self):
      Parameters(self, 50, 120)
        
    def save(self):

        files = [('File CSV', '*.csv')]
        
        self._saved_file = fd.asksaveasfile(  parent = self, 
                                              filetypes= files)
        
    def load_first(self):
      files = [('File CSV', '*.csv')]

      self._first_loaded_file = fd.askopenfile( title= 'Carica il primo file',
                                                parent= self, 
                                                filetypes= files )
      
      if (self._first_loaded_file != None):

            try:

              if (len(self._csv_preview.tabs()) >= 2):
                self._csv_preview.forget(1)

              self._csv_preview.hide(0)

              # display first filename
              self._first_file_name.set(self._first_loaded_file.name.rsplit("/")[-1])

              # Before this we need to choose the separator

              sep = self._first_sep.get()

              data1 = pd.read_csv(  self._first_loaded_file,
                                    dtype= str,
                                    sep= sep,
                                    low_memory=False)
              
              self.draw_preview(  data1, self._first_file_name.get().split('.')[0], 1)

            except:

              error = Error(  self, 'Inserisci il separatore corretto!')

              error.grab_set()

              self.reset(1)

    def load_second(self):
      files = [('File CSV', '*.csv')]
      
      self._second_loaded_file = fd.askopenfile(  title= 'Carica il secondo file',
                                                  parent= self, 
                                                  filetypes= files )
      
      if (self._second_loaded_file != None):
        # display second filename
        try:
          
          if (len(self._csv_preview.tabs()) >= 3):
             self._csv_preview.forget(2)
          
          self._csv_preview.hide(0)

          self._second_file_name.set(self._second_loaded_file.name.rsplit("/")[-1])
                    
          sep = self._second_sep.get()

          data2 = pd.read_csv(  self._second_loaded_file,
                                dtype= str,
                                sep= sep,
                                low_memory= False)
          
          self.draw_preview(data2, self._second_file_name.get().split('.')[0], 2)  

        except:

          error = Error(self, 'Inserisci il separatore corretto!')

          error.grab_set()

          self.reset(2)
       
    def load(self):
                
        # load first file
        if (self._first_loaded_file == None):

          self.load_first()

        if(self._second_loaded_file == None and self._first_loaded_file != None):

          self.load_second()
          self._carica.config(state= tk.DISABLED)
    
    def create_list(self):
      class_list = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['functions.functions']) if inspect.isclass(cls_obj)]
      remove_list = [ 'ABCMeta', 
                      'Error',
                      'Function',
                      'MainWindow',
                      'Parameters',
                      'ThreadPool',
                      'Window',
                      'main']
      functions_list = []

      for name in remove_list:
        class_list.remove(name)
      
      for i in class_list:
        # Suppose we have a module called "math" with a function called "sqrt"
        # We don't know the name of the function in advance, so we use a variable to store it

        # Use globals() to retrieve the function from the global namespace
        func = globals()[i]
        functions_list.append(func)

      return functions_list

if __name__ == "__main__":
    print(dir(functions))
    app = App()
    app.mainloop()
