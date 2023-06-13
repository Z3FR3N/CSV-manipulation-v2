import pandas as pd
from main import App as main
from abc import ABCMeta, abstractmethod

# Function serves as an abstract class to initialize a general function which will be implemented in functions_types

class Function(metaclass= ABCMeta):
    def __init__(self, name: str):
      self._name = name
      self._data1 = main.data1
      self._data2 = main.data2
      self._result = pd.DataFrame
    
    @property
    def name(self):
        return self._name
    
    @property
    def result(self):
        return self._result
    
    @abstractmethod
    def take_parameters(self):
        pass
        
    @abstractmethod
    def generate(self):
        pass
    
    @abstractmethod
    def export(self):
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