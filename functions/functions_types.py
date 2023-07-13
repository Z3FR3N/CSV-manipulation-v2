from functions.function import Function, main
from tkinter import Radiobutton, StringVar, IntVar
from tkinter.ttk import Combobox, Frame, Label, Separator, Button, Checkbutton, Entry
from tkinter.constants import NSEW, EW, E, W
from dialogs.dialogs import Parameters, Error, ScrollableFrame
from pandas import DataFrame, StringDtype
from threading import Thread
from queue import Empty, Queue
import numpy as np
import datetime as dt
import time

""" CODE RESTRUCTURING NEEDED """

# functions_types contains every data-manipulating class
# We need to use the data getters every time we need data -> Dataframes are not memory safe.
# TODO: -Create an API to dinamically import functions from files in a folder
#       - Return a Dataframe with missing/errors
#       - A Function to analize some parameters of the csvs

class Multiple_search(Function):
    """ A class capable of confronting  """
    class  Cells_comparison(Thread): # this does the heavy lifting
      def __init__(self, queue : Queue):
        super().__init__(daemon=True)
        
        self.queue = queue
        
        try:
          self.column2_index = self.queue.get()
          self.column2_list = self.queue.get()
          self.column1_index = self.queue.get()
          self.data_array2 = self.queue.get()
          self.data_array1 = self.queue.get()
          print('queue inizializzata')
        except Empty:
          print('Queue non inizializzata')

        self.match = []
        self.rejected = []
      
      # we can calculate the amount of comparisons and communicate to the mainloop throught the queue: https://www.youtube.com/watch?v=ghSDvtVJPck
      
      def run(self):
        print('entrato in run')
        for row in self.data_array1:
          cell1 = row[self.column1_index]
          self.rejected.append(cell1)
          for row2 in self.data_array2:
            cell2 = row2[self.column2_index]
            if str(cell1) == str(cell2):
              self.match.append(row2)
              self.rejected.remove(cell1)
        print('fatto')
        self.result = DataFrame(self.match, columns = self.column2_list, dtype=object)
        
        self.queue.put(self.rejected)
        self.queue.put(self.result)

    def __init__(self, main_window : main):
      super().__init__('Ricerca multipla', main_window)

    def update_data(self):
      super().update_data()

      self.selection1.config(values= self.csv_available)
      self.selection1.current(0)
      self._selected_csv1.set(self.csv_available[0])
      self.selection2.config(values= self.csv_available)
      
      try:
        self.selection2.current(1)
        self._selected_csv2.set(self.csv_available[1])
      except:
        self.selection2.current(0)
        self._selected_csv2.set(self.csv_available[0])
      
      for widgets in self.first_scrollable.interior.winfo_children():
        widgets.destroy()
      
      for widgets in self.second_scrollable.interior.winfo_children():
        widgets.destroy()

    def take_data(self):
      return super().take_data()
    
    def take_parameters(self):
      super().take_parameters()

      #Initializing the main frame, didving in two section
      self.main_frame.grid_columnconfigure(0, weight=1, minsize= self._window.winfo_reqwidth())

      for n in [0,1]:
        self.main_frame.grid_rowconfigure(0, weight= 1) # To allocate labels and Comboboxes

      # Top Frame: to choose CSVs
      self.top_frame = Frame(self.main_frame)
      self.top_frame.grid(column=0, row= 0, pady= 3, sticky=NSEW)
      
      for n in [0,1,2]:
        self.top_frame.grid_columnconfigure(n, weight= 1)
      
      for n in [0,1]:
        self.top_frame.grid_rowconfigure(n, weight=1, pad= 3)
      
      self.top_frame.grid_rowconfigure(2, weight=1)

      # Labels
      self.label1 = Label(self.top_frame, text= 'CSV 1: ')
      self.label1.grid(row=0, column= 0, sticky= E)

      self.label2 = Label(self.top_frame, text= 'CSV 2: ')
      self.label2.grid(row= 1, column= 0, sticky= E)

      # Comboboxes
      self._selected_csv1 = StringVar()
      self._selected_csv2 = StringVar()

      self.selection1 = Combobox(self.top_frame, values= self.csv_available, textvariable= self._selected_csv1)
      self.selection1.current(0)
      self.selection1.grid(row=0, column=1, sticky= W)

      self.selection2 = Combobox(self.top_frame, values= self.csv_available, textvariable= self._selected_csv2)

      try:
        self.selection2.current(1)
      except:
        self.selection2.current(0)

      self.selection2.grid(row=1, column=1, sticky=W)

      self.read_button = Button(self.top_frame, text='Leggi', command= self.read)
      self.read_button.grid(row=0, column= 2, rowspan= 2)
      
      separator = Separator(self.top_frame)
      separator.grid(row=2, column=0, columnspan=3, sticky= EW)

      # Bottom Frame: to choose Column key names
      self.bottom_frame = Frame(self.main_frame)
      self.bottom_frame.grid(row= 1, column= 0, sticky=NSEW)
      
      self.bottom_frame.grid_rowconfigure(0, weight=1)
      for n in [0,1]:
        self.bottom_frame.grid_columnconfigure(n, weight=1, minsize= self.main_frame.winfo_reqwidth() /2)

      # Two scrollableFrame to display columns
      self.main_frame.update_idletasks()

      height = self._window.winfo_reqheight() - self.main_frame.winfo_reqheight() - self._window.bottom_frame.winfo_reqheight()
      
      self.first_scrollable = ScrollableFrame(self.bottom_frame, height)
      self.first_scrollable.grid(row= 0, column= 0, sticky= NSEW)

      self.second_scrollable = ScrollableFrame(self.bottom_frame, height)
      self.second_scrollable.grid(row= 0, column= 1,sticky= NSEW)

    def read(self):
      csv1 = self._selected_csv1.get()
      csv2 = self._selected_csv2.get()

      if csv1 == csv2:
        Error(self._window, 'Selezionare file diversi!')

      else:
        # variables for Radiobuttons
        self.column_chosen1 = StringVar()
        self.column_chosen2 = StringVar()
        self.column_chosen1.set(" ")
        self.column_chosen2.set(" ")
        self.data_chosen1 = DataFrame(self._data_map[csv1]) # selection data from the map
        self.data_chosen2 = DataFrame(self._data_map[csv2]) # selection data from the map
        self.column_list1 = self.data_chosen1.columns.tolist()
        self.column_list2 = self.data_chosen2.columns.tolist()
        
        width = 105 # limiting buttons size
        
        n_row = 0
        for name in self.column_list1:
          Radiobutton(self.first_scrollable.interior,wraplength=width, variable=self.column_chosen1,value= name, text= str(name)).grid(row=n_row, column=0 , sticky= W)
          n_row += 1
        
        n_row = 0
        for name in self.column_list2:
          Radiobutton(self.second_scrollable.interior, wraplength=width, variable=self.column_chosen2, value= name, text= str(name)).grid(row=n_row, column=0, sticky= W)
          n_row += 1
    
    def generate(self):
      self.queue = Queue() # FIFO structure, for Thread communication
      self.queue.put(self.column_list2.index(self.column_chosen2.get()))
      self.queue.put(self.column_list2)
      self.queue.put(self.column_list1.index(self.column_chosen1.get()))
      self.queue.put(self.data_chosen2.to_numpy(na_value="DTP", dtype=StringDtype))
      self.queue.put(self.data_chosen1.to_numpy(na_value="DTP", dtype=StringDtype))
      # generate an event in the mainloop to display Loading window
      #self._window.event_generate("<<CheckQueue>>")
      self.thread = self.Cells_comparison(self.queue)
      self.thread.start()
      banana = self.queue.get()
      banana2 = self.queue.get()
      print(banana2.head())
      print(len(banana))
          
    def export(self):
      # Aggiungere ai risultati il CSV generato
      # Esportare i valori scartati
      return super().export()

    def info(self):
      return super().info()

class Columns_selection(Function):
  def __init__(self, main_window : main):
    super().__init__('Selezione colonne', main_window)

  def take_data(self):
      return super().take_data()
  
  def update_data(self):
    return super().update_data()

  def take_parameters(self):
    super().take_parameters()

    # Variabile che indica la scelta
    self._selected_csv = StringVar()
    
    self._window.main_frame.grid_columnconfigure(0, weight=1)
    self._window.main_frame.grid_rowconfigure(0, weight=2)
    self._window.main_frame.grid_rowconfigure(1, weight=1)
    self._window.main_frame.grid_rowconfigure(2, weight=1)
    self._window.main_frame.grid_rowconfigure(3, weight=1)
    self._window.main_frame.grid_rowconfigure(4, weight=2)
    
    
    self.top_frame = Frame(self.main_frame)

    self.csv_label = Label(self.top_frame, text= 'CSV: ')
    self.csv_label.grid(column=0, row=0)

    self.choices = Combobox( self.top_frame, 
                              textvariable= self._selected_csv,
                              values= self.csv_available)
        
    self.choices.grid(column= 1, row=0)

    self.csv_button = Button(self.top_frame, text='Leggi', command= self.read)
    self.csv_button.grid(column=2, row= 0, padx= 5, pady= 2)
    self.top_frame.grid(column= 0, row= 0)
    
    self.bottom_frame = Frame(self.main_frame)
    self.csv_label2 = Label(self.bottom_frame, text= 'Nome nuovo CSV: ')
    self.csv_entry = Entry(self.bottom_frame, textvariable= self._result_name)
    self.bottom_frame.grid(column=0, row=4, pady= 2)

    # Adding separators

    self.separatore = Separator(self.main_frame, orient='horizontal')
    self.separatore.grid(column=0, row=1, sticky='EW')

    self.separatore2 = Separator(self.main_frame, orient='horizontal')
    self.separatore2.grid(column=0, row=3, sticky='EW')
   
    # Il secondo cambia la vista in base ai valori
    self.mid_frame = Frame(self.main_frame)
    self.mid_frame.grid_columnconfigure(0, weight=1, minsize=300)
    self.mid_frame.grid_rowconfigure(0, weight= 1)
    self._window.update_idletasks() # to catch the right amount of width and height
    self.scrollable = ScrollableFrame(self.mid_frame, ( self._window.winfo_reqheight() - 
                                                        self.top_frame.winfo_reqheight() -
                                                        self.separatore.winfo_reqheight() -
                                                        self.bottom_frame.winfo_reqheight() - 
                                                        self._window.bottom_frame.winfo_reqheight() - 20)) #defining height

    self.scrollable.grid(column= 0, row=0, sticky=NSEW)
    self.mid_frame.grid(column=0, row=2, sticky=EW)

    self.csv_label2.grid(column=0, row=0, sticky=W)
    self.csv_entry.grid(column=1, row=0)
    
  def read(self):
    # Prelevo il Dataframe
    try:
      csv = self._selected_csv.get()
      self._dataframe_chosen = DataFrame(self._data_map[csv])
      self._columns_list = self._dataframe_chosen.columns.values.tolist()
    except:
      Error(self._window, 'Qualcosa è andato storto')
    
    self._chosen = [] # Create a list of IntVar as big as column_list
    grid_row = 0 # Counter
    self._window.update_idletasks() # Updating width/heigt flags
    
    for i in range(len(self._columns_list)):
      self.value = IntVar()
      self.check = Checkbutton(self.scrollable.interior, onvalue=1, offvalue=0, text = self._columns_list[i], variable = self.value)
      self._chosen.append(self.value)
      self.check.grid(column= 0, row= grid_row, padx= (((self._window.winfo_reqwidth() - 
                                                         self.check.winfo_reqwidth() - 
                                                         self.scrollable.vscrollbar.winfo_reqwidth()) / 2))) # Defining padding
      grid_row+= 1
    
  def generate(self):# Taking column_list and giving the resulting Dataframe

    self._final_col_names = [] # final list

    # Filtering the columns list
    for i in range(len(self._chosen)):
      if self._chosen[i].get() == 1:
        self._final_col_names.append(str(self._columns_list[i]))

    # Filtering the Dataframe
    self._result = self._dataframe_chosen[self._final_col_names].copy()
    return self.export()
    
  def export(self):
    return super().export()
  
  def info(self):
    return super().info()

class Renames_columns(Function):
# restituire un dataframe con le voci scartate
    def __init__(self, main_window : main):
      super().__init__('Rinomina Colonne', main_window)

    def update_data(self):
      return super().update_data()
    
    def take_data(self):
      return super().take_data()
    
    def take_parameters(self):
      print(self.name)
      super().take_parameters()

    def generate(self):
      # TODO: Filtrare le colonne chiave, generare il DataFrame utilizzando Loading
      print('do something')

    def export(self):
      # TODO: Utilizzare Columnsselection per scegliere le colonne
      return super().export()

    def info(self):
      return super().info()

class String_length_check(Function):
# restituire un dataframe con le voci scartate
    def __init__(self, main_window : main):
      super().__init__('Lunghezza colonne', main_window)

    def update_data(self):
      return super().update_data()
    
    def take_data(self):
      return super().take_data()
    
    def take_parameters(self):
      super().take_parameters()

      # Variabile che indica la scelta
      self._selected_csv = StringVar()

      self._window.main_frame.grid_columnconfigure(0, weight=1)
      self._window.main_frame.grid_rowconfigure(0, weight=2)
      self._window.main_frame.grid_rowconfigure(1, weight=1)
      self._window.main_frame.grid_rowconfigure(2, weight=1)
      self._window.main_frame.grid_rowconfigure(3, weight=1)
      self._window.main_frame.grid_rowconfigure(4, weight=2)


      self.top_frame = Frame(self.main_frame)

      self.csv_label = Label(self.top_frame, text= 'CSV: ')
      self.csv_label.grid(column=0, row=0)

      self.choices = Combobox( self.top_frame, 
                                textvariable= self._selected_csv,
                                values= self.csv_available)

      self.choices.grid(column= 1, row=0)

      self.csv_button = Button(self.top_frame, text='Leggi', command= self.read)
      self.csv_button.grid(column=2, row= 0, padx= 5, pady= 2)
      self.top_frame.grid(column= 0, row= 0)

      self.bottom_frame = Frame(self.main_frame)
      self.csv_label2 = Label(self.bottom_frame, text= 'Nome nuovo CSV: ')
      self.csv_entry = Entry(self.bottom_frame, textvariable= self._result_name)
      self.bottom_frame.grid(column=0, row=4, pady= 2)

      # Adding separators

      self.separatore = Separator(self.main_frame, orient='horizontal')
      self.separatore.grid(column=0, row=1, sticky='EW')

      self.separatore2 = Separator(self.main_frame, orient='horizontal')
      self.separatore2.grid(column=0, row=3, sticky='EW')

      # Il secondo cambia la vista in base ai valori
      self.mid_frame = Frame(self.main_frame)
      self.mid_frame.grid_columnconfigure(0, weight=1, minsize=300)
      self.mid_frame.grid_rowconfigure(0, weight= 1)
      self._window.update_idletasks() # to catch the right amount of width and height
      self.scrollable = ScrollableFrame(self.mid_frame, ( self._window.winfo_reqheight() - 
                                                          self.top_frame.winfo_reqheight() -
                                                          self.separatore.winfo_reqheight() -
                                                          self.bottom_frame.winfo_reqheight() - 
                                                          self._window.bottom_frame.winfo_reqheight() - 20)) #defining height

      self.scrollable.grid(column= 0, row=0, sticky=NSEW)
      self.mid_frame.grid(column=0, row=2, sticky=EW)

      self.csv_label2.grid(column=0, row=0, sticky=W)
      self.csv_entry.grid(column=1, row=0)

    def read(self):
      # Prelevo il Dataframe
      try:
        csv = self._selected_csv.get()
        self._dataframe_chosen = DataFrame(self._data_map[csv])
        self._columns_list = self._dataframe_chosen.columns.values.tolist()
      except:
        Error(self._window, 'Qualcosa è andato storto')

      self._chosen = [] # Create a list of IntVar as big as column_list
      grid_row = 0 # Counter
      self._window.update_idletasks() # Updating width/heigt flags
      

    def generate(self):
      # TODO: Filtrare le colonne chiave, generare il DataFrame utilizzando Loading
      print('do something')

    def export(self):
      # TODO: Utilizzare Columnsselection per scegliere le colonne
      return super().export()

    def info(self):
      return super().info()
    