import pandas as pd
from main import App as main
from abc import ABCMeta, abstractmethod

# Function serves as an abstract class to initialize a general function which will be implemented in functions_types

class Function(metaclass= ABCMeta):
    def __init__(self, name: str):
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
    def take_parameters(self):
        print('construct a child parameter to take input')
        

    @abstractmethod
    def generate(self):
        print('do something')
    
    def __str__(self):
        return str(self._name)
    
    def __eq__(self, __value: object) :
        if (isinstance(__value, Function)):
            return self.name == __value.name
        if (isinstance(__value, str)):
            return self.name == __value
        else:
            raise TypeError