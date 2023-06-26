from sys import modules
from io import IOBase
from inspect import ismethod, getmembers, isclass
from tkinter import LabelFrame, StringVar
from pandas import DataFrame, read_csv
from tkinter.ttk import Frame, Button, Combobox, Radiobutton, Notebook, Label
from tkinter.filedialog import askopenfile, asksaveasfile
from main_settings import MainWindow
from pandastable import Table # plotting a table from a DataFrame
from dialogs.dialogs import Error
from functions.functions_types import * # wildcard is necessary, this is a mutable module
# import customtkinter as ctk -> can be useful for restyling

"""
  TODO: - Code optimization through Loop and better Attributes assignment
        - Give the user the option to save the file also as excel format and to choose tje separator
        - Finish generate()
        - Implementing functions
        - Better naming convention
        - Poor encapsulation: lol -> i'm new at OOP
"""

class App(MainWindow):
    _data1 = DataFrame()
    _data2 = DataFrame()
    _results = []

    def __init__(self):
        super().__init__('Manipolazione CSV', 550, 500, 400, "ICO.png", 30 )
        
        self._function_list = []
        self._function_list_names = []
        self._results_names = []
        self.create_list()
        self._first_file_name = StringVar(value= 'Nessun File caricato.')
        self._second_file_name = StringVar(value= 'Nessun File caricato.')
        self._first_sep = StringVar(value=" ")
        self._second_sep = StringVar(value=" ")
        self._selected_function = StringVar(value=" ")
        self._first_loaded_file = None
        self._second_loaded_file = None

        # Adding interface's elements, most complex ones with dedicated method
        self.create_widgets()

        # Initially, preview will be empty
        self.reset() 
        
        # Always create the grid AFTER widgets
        self.create_grid()
    
    # Getter

    def set_results(self, data: DataFrame, name : str):
       if data.empty == True:
        Error(self, 'Nessun dato generato')
       else:
        self._results.append(data)
        self._results_names.append(str(name))
    
    def get_data1(self):
        return self._data1
    
    def get_data2(self):
        return self._data2

    @property
    def results_names(self):
       return self._results_names

    @property
    def first_file_name(self):
      return self._first_file_name.get()
    
    @property
    def second_file_name(self):
      return self._second_file_name.get()
    
    # METHODS

    def create_widgets(self):

        self._main_frame = Frame( self, relief='flat')

        # Buttons of the main view
        
        self._reset = Button( self._main_frame, text='Reset', command= self.reset)
        
        self._inverti = Button( self._main_frame, text='Inverti', command= self.switch)
        
        self._carica = Button( self._main_frame, text='Carica CSV', command= self.load)
        
        self._salva = Button( self._main_frame, text= 'Salva', command = self.save, state='disabled')
        
        self._info = Button( self._main_frame, text= 'Info', command= self.info)
        
        self._genera = Button(  self._main_frame, text= 'Genera', command= self.generate)

        # Combobox for selecting the function to launch

        # Identify the right function

        self._functions_frame = Frame(self._main_frame)
        
        self._functions_text = Label( self._functions_frame,
                                      text= "Lista funzioni: ",
                                      justify= 'left',
                                      anchor='center')

        self._functions_cbox = Combobox(  self._functions_frame, 
                                          textvariable= self._selected_function,
                                          # values: lists of functions available
                                          values= self._function_list_names,
                                          width= self._combobox_width)
        
        self._functions_text.grid(row= 0, column= 0, sticky= ('E'), padx= 5)
        self._functions_cbox.grid(row= 0, column= 1, sticky=('W'))

        self._functions_frame.rowconfigure(0, weight=1)
        self._functions_frame.columnconfigure(0, weight= 1)
        self._functions_frame.columnconfigure(1, weight=1)

        # Due sezioni con LabelFrame da riempire con il nome dei file caricati
        
        self._first_name = LabelFrame(  self._main_frame, 
                                        text= 'CSV 1',
                                        labelanchor='n',
                                        relief= 'groove')
        
        self._display_name1 = Label(  self._first_name, 
                                      textvariable= self._first_file_name,
                                      justify= 'center',
                                      anchor='center',
                                      padding= 3)
        
        self._second_name = LabelFrame( self._main_frame, 
                                        text='CSV 2',
                                        labelanchor='n',
                                        relief= 'groove')
        
        self._display_name2 = Label(  self._second_name, 
                                      textvariable= self._second_file_name,
                                      justify= 'center',
                                      anchor='center',
                                      padding= 3)

        self._sep_text1 = Label(  self._first_name, text= 'Separatore:')
        
        self._sep_text2 = Label(  self._second_name, text= 'Separatore:')
        
        self._first_sep_dotcomma = Radiobutton( self._first_name,
                                                text=';',
                                                variable= self._first_sep,
                                                value= ';')
        
        self._load_first = Button(  self._first_name, text= 'Carica CSV 1', command= self.load_first)
        
        self._load_second = Button( self._second_name,
                                    text= 'Carica CSV 2',
                                    command= self.load_second)
        
        # setting default separator
        self._first_sep_dotcomma.invoke()
        
        self._first_sep_comma = Radiobutton(  self._first_name,
                                              text=',',
                                              variable= self._first_sep,
                                              value= ',')
                
        self._second_sep_dotcomma = Radiobutton(  self._second_name,
                                                  text=';',
                                                  variable= self._second_sep,
                                                  value= ';')
        
        self._second_sep_comma = Radiobutton( self._second_name,
                                              text=',',
                                              variable= self._second_sep,
                                              value= ',')
        
        # setting default separator
        self._second_sep_dotcomma.invoke()
        
        # Notebook for preview

        self._csv_preview = Notebook( self._main_frame)

    def create_grid(self):
        
        self._main_frame.grid(  column=0, row=0, sticky=('NSEW') )
        
        # Row 1

        self._functions_frame.grid( column= 1,
                                    row= 0,
                                    columnspan= 2,
                                    sticky=('EW'),
                                    pady= 5 )

        self._info.grid(  column= 0, row= 0, pady= 5  )

        self._genera.grid(  column= 3, row= 0, pady= 5  )
        
        # Row 2

        self._csv_preview.grid( column= 0,
                                row= 1,
                                columnspan= 4,
                                pady= 5,
                                padx= 2,
                                sticky=('NSEW') )
        
        # Row 3
        
        # Placing objects inside the first Labelframe

        self._sep_text1.grid( column= 0, row= 1, sticky= 'E' )
        
        self._first_sep_dotcomma.grid(  row= 1, column= 1 )
        
        self._first_sep_comma.grid( row= 1, column= 2, sticky= 'W')
        
        self._display_name1.grid( row= 0, column= 0, columnspan= 3)
        
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
        
        self._sep_text2.grid(   column= 0, row= 1, sticky= 'E' )
        
        self._second_sep_dotcomma.grid( row= 1, column= 1 )
        
        self._second_sep_comma.grid(  row= 1, column= 2, sticky= 'W')
        
        self._load_second.grid( column= 0,
                                row= 2,
                                sticky=('NSEW'),
                                columnspan= 3)
        
        self._display_name2.grid( row= 0, column= 0, columnspan= 3)
        
        # LabelFrame ready
        
        self._second_name.grid( column= 2,
                                row= 2,
                                columnspan= 2,
                                sticky= ('EW'),
                                padx= 5,
                                pady= 5)
        
        # Configure rows and columns to display the labelframe
        
        self._first_name.rowconfigure(  0, weight= 1, pad=2)
        
        self._first_name.rowconfigure(  1, weight= 1, pad=2)

        self._first_name.rowconfigure(  2, weight= 1, pad=2)

        self._first_name.columnconfigure( 0, weight= 1)

        self._first_name.columnconfigure( 1, weight= 1)

        self._first_name.columnconfigure( 2, weight= 1)

        self._second_name.rowconfigure( 0, weight= 1, pad=2)
        
        self._second_name.rowconfigure( 1, weight= 1, pad=2)
        
        self._second_name.rowconfigure( 2, weight= 1, pad=2)
        
        self._second_name.columnconfigure(  0, weight= 1)
        
        self._second_name.columnconfigure(  1, weight= 1)
        
        self._second_name.columnconfigure(  2, weight= 1)

        # Row 4

        self._reset.grid( column= 0, row= 3, pady= 5)

        self._inverti.grid( column= 1, row= 3, pady= 5 )

        self._carica.grid(  column= 2, row= 3, pady= 5 )

        self._salva.grid(   column= 3, row= 3, pady= 5)

        # weights for resizing and to initialize spacing

        self.columnconfigure( 0, weight=1, pad= 5)  # self._main_frame
        
        self.rowconfigure(  0, weight=1, pad= 5)     # self._main_frame
        
        self._main_frame.columnconfigure( 0, weight=1, pad= 3)

        self._main_frame.columnconfigure( 1, weight=3, pad= 3)
        
        self._main_frame.columnconfigure( 2, weight=3, pad= 3) 
        
        self._main_frame.columnconfigure( 3, weight=1, pad= 3)
        
        self._main_frame.rowconfigure(  1, weight= 5)      

    def clean_preview(self, count = 0):
      for i in self._csv_preview.tabs():
          self._csv_preview.forget(i)

      # No Preview
      self._no_preview = Frame( self._csv_preview)
      self._no_preview_loaded = Label(  self._no_preview, 
                                        text='Nessun file caricato')
      
      self._no_preview_loaded.place(  relx=0.5, 
                                      rely=0.5, 
                                      anchor='center')
      
      self._csv_preview.add(self._no_preview, text= 'No csv')
      
      if (len(self._csv_preview.tabs()) > 1 and count <= len(self._csv_preview.tabs())):
        self._csv_preview.forget(count)

    def draw_preview(self, data : DataFrame, name: str, position : int):

      # DataFrame loaded
      self._csv = Frame(  self._csv_preview, relief= 'flat')   
      
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
      
    def switch(self):
        
        if(self._first_loaded_file != None and self._second_loaded_file != None and len(self._csv_preview.tabs()) > 2):

          tmp = self._first_loaded_file
          self._first_loaded_file = self._second_loaded_file
          self._second_loaded_file = tmp

          tmp = StringVar()
          tmp.set(self._first_file_name.get())
          self._first_file_name.set(self._second_file_name.get())
          self._second_file_name.set(tmp.get())

          tmp = self._csv_preview.tabs()[2]
          self._csv_preview.insert(1, tmp)
          self._csv_preview.select(1)
          
        else:
          Error(self, "Carica i due CSV!")

    def info(self):
      #colonna = ColumnsComparison(self) # always instanciate to use properties
      print('banana')

    def reset(self, count = 0):
        
        if (count == 0):
          self._first_loaded_file = None
          self._second_loaded_file = None
          self._results.clear()

          self._first_file_name.set('Nessun File caricato.')
          self._second_file_name.set('Nessun File caricato.')

          self.clean_preview()
          self._carica.config(state= '!disabled')

        if (count == 1):
           self._first_loaded_file = None
           self._first_file_name.set('')
           self.clean_preview()
           self._genera.state(['disabled'])
           self._results.clear()

        if (count == 2):
           self._second_loaded_file = None
           self._second_file_name.set('')
           self.clean_preview(count)
           self._results.clear()

    def generate(self):
      #try:
          for fun in self._function_list:
            if fun.__eq__(self._selected_function.get()) and ismethod(fun.take_parameters):
              fun.take_parameters()
              if (len(self._results) > 0):
                self._salva.state(['!disabled'])
              break
      #except:
      #        Error(self, 'Inserisci una funzione valida!')
    
    def save(self):
        name = self._csv_preview.tab(self._csv_preview.select(), "text")
        if (len(self._results) > 0):
          files = [('File CSV', '*.csv')]

          path = asksaveasfile(   parent = self, 
                                  filetypes= files,
                                  title= 'Salva con nome',
                                  confirmoverwrite= True,
                                  initialfile= name)
          if (path != None):
            name.to_csv(path, index=False, lineterminator='\n', encoding='utf-8', sep=';')
          else:
             Error(self, 'Indica un file!')
         
    def load_first(self):
      files = [('File CSV', '*.csv')]

      self._first_loaded_file = askopenfile(  title= 'Carica il primo file',
                                              parent= self, 
                                              filetypes= files )
      
      if (isinstance(self._first_loaded_file, IOBase)):

            try:

              if (len(self._csv_preview.tabs()) >= 2):
                self._csv_preview.forget(1)

              self._csv_preview.hide(0)

              # display first filename
              self._first_file_name.set(self._first_loaded_file.name.rsplit("/")[-1])

              # Before this we need to choose the separator

              sep = self._first_sep.get()

              self._data1 = read_csv( self._first_loaded_file,
                                      dtype= str,
                                      sep= sep,
                                      low_memory=False)
              
              self.draw_preview( self._data1, self._first_file_name.get().split('.')[0], 1)
              self._genera.state(['!disabled'])

            except:

              Error(self, 'Inserisci il separatore corretto!')

              self.reset(1)

    def load_second(self):
      files = [('File CSV', '*.csv')]
      
      self._second_loaded_file = askopenfile(   title= 'Carica il secondo file',
                                                parent= self, 
                                                filetypes= files )
      
      if (isinstance(self._second_loaded_file, IOBase)):
        # display second filename
        try:
          
          if (len(self._csv_preview.tabs()) >= 3):
             self._csv_preview.forget(2)
          
          self._csv_preview.hide(0)

          self._second_file_name.set(self._second_loaded_file.name.rsplit("/")[-1])
                    
          sep = self._second_sep.get()

          self._data2 = read_csv(   self._second_loaded_file,
                                    dtype= str,
                                    sep= sep,
                                    low_memory= False)
          
          self.draw_preview(self._data2, self._second_file_name.get().split('.')[0], 2)
          self._genera.state(['!disabled'])

        except:

          Error(self, 'Inserisci il separatore corretto!')

          self.reset(2)
       
    def load(self):

      self.load_first()
      self.load_second()
    
    def create_list(self):
      for name, obj in getmembers(modules[__name__]):
          if isclass(obj):
            # avoid instanciating known classes:
            if name in ['Error', 'Function', 'Image', 'ImageTk', 
                        'MainWindow', 'Table' 'Loading',
                        'Parameters', 'ThreadPool', 'App']:
               continue
            else:
              try:
                self._function_list_names.append(str(obj(self).name))
                self._function_list.append(obj(self))
              except:
                 continue
      
      self._combobox_width = 0
      for name in self._function_list_names:
         if len(name) > self._combobox_width:
            self._combobox_width = len(name)
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
