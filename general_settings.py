from tkinter import Widget
from queue import Queue

""" Fixing a strange issue where i can't assign tuples to grid_[row/column]configure, be careful: doesn't check the coerence of the given parameters """

def multirowconfigure(widget : Widget,  rows: list[int], **param):
  """
  Enable multiple rows configuration
  """
  for i in rows:
    widget.grid_rowconfigure(index= i,  **param)

def multicolumnconfigure(widget : Widget,  columns: list[int] , **param ):
  """
  Enable multiple columns configuration
  """
  for i in columns:
    widget.grid_columnconfigure(index= i,  **param)

def loadqueue(queue: Queue, items : list):
  """
  Load multiple items on a queue
  """
  for item in items:
    queue.put(item)
  