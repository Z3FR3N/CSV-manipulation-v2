from dialogs.dialogs import *
import pandas as pd
from main import App as main
from abc import ABCMeta, abstractmethod

# Function serves as an abstract class to initialize a general function

class Function(Parameters, metaclass= ABCMeta):
    def __init__(self, name: str, main_window : MainWindow, height : int, width: int):
      super().__init__(main_window, height, width)
      self._name = name
      self._data1 = main.first_file
      self._data2 = main.second_file
      self._result = pd.DataFrame
      self._sep1 = main.first_separator
      self._sep2 = main.second_separator
    
    @property
    def name(self):
        return self._name
    
    @property
    def result(self):
        return self._result
    
    @abstractmethod
    def generate(self):
        pass