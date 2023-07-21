from dialogs.dialogs import Parameters, Error, Frame, NSEW
from main import CSV_Toolkit as main
from main import DataFrame, StringVar
from abc import ABCMeta, abstractmethod

# Function serves as an abstract class to initialize a general function which will be implemented in functions_types

class Function(metaclass= ABCMeta):
    
    def __init__(self, name: str, main_window : main):
      self._name = name
      self._main_window = main_window
      self._result = DataFrame()
      self._result_name = StringVar()
    
    @property
    def name(self):
       return self._name
    
    @property
    def main_window(self):
       return self._main_window
    
    @abstractmethod
    def take_data(self):
       # Get input Dataframe
      self._data1 = self.main_window.get_data1() 
      self._data2 = self.main_window.get_data2()

      # Get their names
      self._first_file_name = self.main_window.first_file_name
      self._second_file_name = self.main_window.second_file_name

      # Initialize name list
      self.csv_available = list()
      self.data_available = list()
      
      # Input checking
      if self._first_file_name != "Nessun CSV caricato" and (not self._first_file_name.isspace()):
        self.csv_available.append(self._first_file_name)
      if self._second_file_name != 'Nessun CSV caricato' and (not self._second_file_name.isspace()):
        self.csv_available.append(self._second_file_name)
      if len(self.main_window.results_names) > 0:
        self.csv_available.extend(self.main_window.results_names)

      # Data validation
      if not self._data1.empty:
        self.data_available.append(self._data1)
      if not self._data2.empty:
        self.data_available.append(self._data2)
      if len(self.main_window._results) > 0:
        self.data_available.extend(self.main_window._results)

      # Associating Data and names
      self._data_map = dict(zip(self.csv_available, self.data_available))
    
    @abstractmethod
    def update_data(self):
      self.take_data()
    
    @abstractmethod
    def take_parameters(self):

      self.take_data()
      
      self._window = Parameters(self._main_window, self)

      # Window initialization
      self.main_frame = Frame(self._window.content) # to allocate content dinamically
      self.main_frame.grid(column=0, row=0, sticky= NSEW)

    @abstractmethod
    def generate(self):
      pass
    
    @abstractmethod
    def export(self):
      # Checking the name for saving and adding to main.results
      self.main_window.add_results(self._result, self._result_name.get())
      self._result = DataFrame()
      self._result_name.set("")

    @abstractmethod
    def info(self):
      pass
    
    def __str__(self):
      return str(self._name)
    
    def __eq__(self, __value: object) :
      if (isinstance(__value, Function)):
          return self.name == __value.name
      if (isinstance(__value, str)):
          return self.name == __value
      else:
          raise TypeError