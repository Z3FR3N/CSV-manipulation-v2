from dialogs.dialogs import Parameters, Loading
from main import App as main
from abc import ABCMeta, abstractmethod

# Function serves as an abstract class to initialize a general function which will be implemented in functions_types

class Function(metaclass= ABCMeta):
    
    def __init__(self, name: str, main_window : main):
      self._name = name
      self._main_window = main_window
    
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
      self._window = Parameters(self.main_window)
        
    @abstractmethod
    def generate(self):
      pass
    
    @abstractmethod
    def export(self):
      # Calls main.set_result()
      pass

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