from dialogs.dialogs import Parameters, Error
from main import App as main
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
    def take_parameters(self):
      self._data1 = self.main_window.get_data1()
      self._data2 = self.main_window.get_data2()
      self._first_file_name = self.main_window.first_file_name
      self._second_file_name = self.main_window.second_file_name
      self._window = Parameters(self._main_window, self)

    @abstractmethod
    def generate(self):
      pass
    
    @abstractmethod
    def export(self):
      # Checking the name for saving and adding to main.results
      return self.main_window.add_results(self._result, self._result_name.get())

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