from threading import Thread
from unittest import result
from functions.function import Function, main
from general_settings import multicolumnconfigure, multirowconfigure, loadqueue
from tkinter import END, Radiobutton, StringVar, IntVar
from tkinter.ttk import Combobox, Frame, Label, Separator, Button, Checkbutton, Entry
from tkinter.constants import NSEW, EW, E, W, HORIZONTAL
from dialogs.dialogs import Parameters, Error, ScrollableFrame
from pandas import DataFrame, StringDtype, Series, concat
from multithreading import Ticket, Ticket_pourpose
from collections import defaultdict
from queue import Empty, Queue
from enum import Enum, auto
from numpy import NaN
import numpy as np
import datetime as dt
import time

# functions_types contains every data-manipulating class
# We need to use the data getters every time we need data -> Dataframes are not thread safe.

""" 
TODO: -Create an API to dinamically import functions from files in a folder
       - Return a Dataframe with missing/errors
       - A Function to analize some parameters of the csvs/Dataframe given
       - A function to split all the columns in a define char
       - A function to unite Dataframes in one csv
       - A function which compare two column and merge the corresponding ones 
"""

class Multiple_search(Function):
  """ 
  Compare one-by-one the values in two columns from two different Dataframes
  """
    
# we can calculate the amount of comparisons and communicate to the mainloop throught the queue: https://www.youtube.com/watch?v=ghSDvtVJPck

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

    multirowconfigure(self.main_frame, [0,1], weight= 1)

    # Top Frame: to choose CSVs
    self.top_frame = Frame(self.main_frame)
    self.top_frame.grid(column=0, row= 0, pady= 3, sticky=NSEW)
    
    multicolumnconfigure(self.top_frame, [0,1,2], weight = 1)

    multirowconfigure(self.top_frame, [0,1], weight=1, pad=3)
    
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
    multicolumnconfigure(self.bottom_frame, [0,1], weight= 1, minsize= self.main_frame.winfo_reqwidth() /2)

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
    numpy1 = self.data_chosen1.to_numpy(na_value= NaN, dtype=StringDtype, copy=True)
    numpy2 = self.data_chosen2.to_numpy(na_value= NaN, dtype=StringDtype, copy=True)
    new_thread = Thread(target=self.task, kwargs={  'queue' : self.main_window.queue,
                                                    'data_array1' : numpy1,
                                                    'column1_index' : self.column_list1.index(self.column_chosen1.get()),
                                                    'data_array2' : numpy2,
                                                    'column2_index' : self.column_list2.index(self.column_chosen2.get()),
                                                    'column2_list' : self.column_list1 + self.column_list2})
    start = time.time()
    new_thread.start()
    end = time.time()
    #self._doubles = self.main_window.queue.get()
    self._rejected = self.main_window.queue.get()
    self._result = self.main_window.queue.get()
    self._result_name.set('Risultato confronto')
    super().export()
    self._result = self._rejected
    self._result_name.set('Rifiutati')
    super().export()
    #self._result = self._doubles
    #self._result_name.set('Duplicati')
    #super().export()

  def task(self, queue : Queue, data_array1, column1_index : int, data_array2, column2_index : int, column2_list : list):
      rejected = []
      matches = []
      rejected_row = []
      doubles = []
      #ticket = Ticket(ticket_type= Ticket_pourpose.START, ticket_value= '')
      #queue.put(ticket)
      #self._main_window.event_generate("<<CheckQueue>>", when='tail')
      for row in data_array1:
        cell1 = str(row[column1_index]).strip()
        rejected.append(cell1)
        rejected_row.append(list(row))
        #ticket = Ticket(ticket_type= Ticket_pourpose.KEEP_ALIVE, ticket_value= '')
        #queue.put(ticket)
        #self._window.event_generate("<<CheckQueue>>")
        count = 1
        count2 = 0
        for match in doubles:
            if cell1 == str(match):
              count+=1
        for row2 in data_array2:
          cell2 = str(row2[column2_index]).strip()
          
          if cell1 == cell2:
            count2+=1

            if((count2 == 1) and (count2 == count)):
              matches.append(list(row) + list(row2))
            
            elif(count2 > count):
              matches.append(list(row) + list(row2))
              doubles.append(cell2)
              
            try:
              rejected.remove(cell1)
              rejected_row.remove(list(row))
            except ValueError:
              continue
            #ticket = Ticket(ticket_type= Ticket_pourpose.KEEP_ALIVE, ticket_value= '')
            #queue.put(ticket)
            #self._main_window.event_generate("<<CheckQueue>>")
      n_cols = len(row) + len(row2)
      cols_names = []
      for i in range(n_cols):
        cols_names.append(str(i))
        #column2_list
      result = DataFrame(matches, columns = cols_names, dtype=object)
      rejected_data = DataFrame(rejected_row, columns=list(self.data_chosen1.columns.values), dtype=object)
      #doubles = DataFrame(doubles, columns=cols_names, dtype= object)
      print('Rifiutati: ', len(rejected))
      print('Trovati: ', len(result))
      #print('duplicati:', len(doubles))
      #queue.put(doubles)
      queue.put(rejected_data)
      queue.put(result)
      #ticket = Ticket(ticket_type= Ticket_pourpose.END_TASK, ticket_value= '')
      #self._main_window.queue.put(ticket)
      #self._main_window.event_generate("<<CheckQueue>>")
        
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

    multirowconfigure(self._window.main_frame, [1,2,3], weight=1)
    multirowconfigure(self._window.main_frame, [0,4], weight=2)
    
    self.top_frame = Frame(self.main_frame)

    self.csv_label = Label(self.top_frame, text= 'CSV: ')
    self.csv_label.grid(column=0, row=0)

    self.choices = Combobox(  self.top_frame, 
                              textvariable= self._selected_csv,
                              values= self.csv_available)
        
    self.choices.grid(column= 1, row=0)

    self.csv_button = Button(self.top_frame, text='Leggi', command= self.read)
    self.csv_button.grid(column=2, row= 0, padx= 5, pady= 2)
    self.top_frame.grid(column= 0, row= 0)
    
    self.bottom_frame = Frame(self.main_frame)
    self.csv_label2 = Label(self.bottom_frame, text= 'Nome nuovo CSV: ')
    self.csv_entry = Entry(self.bottom_frame, textvariable= self._result_name)
    self.bottom_frame.grid( column=0, row=4, pady= 2)

    # Adding separators

    self.separatore = Separator(self.main_frame, orient=HORIZONTAL)
    self.separatore.grid( column=0, row=1, sticky=EW)

    self.separatore2 = Separator(self.main_frame, orient=HORIZONTAL)
    self.separatore2.grid(  column=0, row=3, sticky=EW)
   
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

    self.scrollable.grid( column= 0, row=0, sticky=NSEW)
    self.mid_frame.grid(  column=0, row=2, sticky=EW)

    self.csv_label2.grid( column=0, row=0, sticky=W)
    self.csv_entry.grid(  column=1, row=0)
    
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
  """
  Restituire un Dataframe con tutte le celle che rispettano i requisiti
  """
  def __init__(self, main_window : main):
    super().__init__('Lunghezza caratteri celle', main_window)

  def update_data(self):
    return super().update_data()
  
  def take_data(self):
    return super().take_data()
  
  def take_parameters(self):
    super().take_parameters()

    # Variabile che indica la scelta
    self._selected_csv = StringVar()

    self._window.main_frame.grid_columnconfigure(0, weight=1)
    multirowconfigure(self._window.main_frame, [1,2,3], weight=1)
    multirowconfigure(self._window.main_frame, [0,4], weight=2)

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

    # Adding separators
    self.separatore = Separator(self.main_frame, orient=HORIZONTAL)
    self.separatore.grid(column=0, row=1, sticky=EW)

    self.separatore2 = Separator(self.main_frame, orient=HORIZONTAL)
    self.separatore2.grid(column=0, row=3, sticky=EW)

    # Bottom Frame
    self.bottom_frame = Frame(self.main_frame)
    self.bottom_frame.grid(column= 0, row= 4, sticky=NSEW)

    self.bottom_label1 = Label(self.bottom_frame, text='Celle maggiori di: ')
    self.bottom_label1.grid(column= 1, row=0, pady= 4)

    multicolumnconfigure(self.bottom_frame, [0, 3], weight= 1)

    self.chosen_lenght = IntVar()
    self.bottom_entry = Entry(self.bottom_frame, textvariable=self.chosen_lenght, width= 6)
    self.bottom_entry.grid(column= 2, row=0, pady=4)

    # Il secondo cambia la vista in base ai valori
    self.mid_frame = Frame(self.main_frame)
    self.mid_frame.grid_columnconfigure(0, weight=1, minsize=300)
    self.mid_frame.grid_rowconfigure(0, weight= 1)
    self._window.update_idletasks() # to catch the right amount of width and height
    self.scrollable = ScrollableFrame(self.mid_frame, ( self._window.winfo_reqheight() - 
                                                        self.top_frame.winfo_reqheight() -
                                                        self.bottom_frame.winfo_reqheight() -
                                                        self.separatore.winfo_reqheight() -
                                                        self._window.bottom_frame.winfo_reqheight())) #defining height

    self.scrollable.grid(column= 0, row=0, sticky=NSEW)
    self.mid_frame.grid(column=0, row=2, sticky=EW)

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
      self.check.grid(column= 0, row= grid_row, padx= ((( self._window.winfo_reqwidth() - 
                                                          self.check.winfo_reqwidth() - 
                                                          self.scrollable.vscrollbar.winfo_reqwidth()) / 2))) # Defining padding
      grid_row+= 1 

  def generate(self):
    try:
      int(self.bottom_entry.get())
    except ValueError:
      self.bottom_entry.delete(0,END)
      return Error(self._window, 'Inserisci un numero!')
    
    columns_counters = list() # name of the columns taken
    columns_names = list()
    counter = 0
    for i in range(len(self._chosen)): # getting the index of the columns
      if self._chosen[i].get() == 1:
        columns_counters.append(counter)
        columns_names.append(str(self._columns_list[i]))
      counter+=1

    data = self._dataframe_chosen.to_numpy(dtype= object, copy= True)
    first_part = list()
    second_part = list()
    indexes = list()
    data1 = list()
    
    #task
    lenght = 0
    for column in columns_counters:
      counter = 2
      first_part.clear()
      second_part.clear()
      indexes.clear()

      for row in data:
        cell = row[column]

        if len(str(cell)) >= self.chosen_lenght.get(): # quì è possibile introdurre il conteggio da destra o da sinistra
          first_part.append(str(cell)[0:self.chosen_lenght.get()])
          second_part.append(str(cell)[self.chosen_lenght.get():-1])
          indexes.append(str(counter))
          
          #if len(found) > lenght: lenght = len(found)
        counter+=1

    columns_dict = {'Prima parte': first_part, 'Seconda parte': second_part, 'Riga': indexes}
    # loc = 0
    # for name, data in a_dict.items():
    #   if (loc % 2 != 0):
    #     self._result.insert(loc, 'RIGA', data, allow_duplicates=True)
    #   else:
    #     self._result.insert(loc, name, data, allow_duplicates=True)
    #   loc+=1
    self._result = DataFrame(columns_dict)
    self._result_name = StringVar(value=('MAGGIORI_DI_' + str(self.chosen_lenght.get())))
    self.export()

  def export(self):
    # TODO: Utilizzare Columnsselection per scegliere le colonne
    return super().export()

  def info(self):
    return super().info()