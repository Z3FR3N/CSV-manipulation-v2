from enum import Enum, auto
from tkinter import Tk
from queue import Queue
from pandas import DataFrame

""" 
A ticket based system that uses queue to communicate the status of the Thread 
"""

class Ticket_pourpose(Enum):
  """ 
  Enum which define various type of the ticket
  """
  START = auto()
  KEEP_ALIVE = auto()
  END_TASK = auto()
  PERCENTAGE = auto()

class Ticket():
  """
  Ticket class -> goes into the queue
  """
  def __init__(self, 
               ticket_type : Ticket_pourpose, 
               ticket_value : str):
    
    self.ticket_type = ticket_type
    self.ticket_value = ticket_type

def task(main_window : Tk, queue : Queue, data_array1, column1_index : int, data_array2, column2_index : int, column2_list : list):
  rejected = []
  match = []
  ticket = Ticket(ticket_type= Ticket_pourpose.START, ticket_value= '')
  queue.put(ticket)
  main_window.event_generate("<<CheckQueue>>", when='tail')
  for row in data_array1:
    cell1 = row[column1_index]
    rejected.append(cell1)
    ticket = Ticket(ticket_type= Ticket_pourpose.KEEP_ALIVE, ticket_value= '')
    queue.put(ticket)
    main_window.event_generate("<<CheckQueue>>",  when='tail')
    for row2 in data_array2:
      cell2 = row2[column2_index]
      if str(cell1) == str(cell2):
        match.append(row2)
        rejected.remove(cell1)
        print(str(cell1) + ' ' + str(cell2))
        ticket = Ticket(ticket_type= Ticket_pourpose.KEEP_ALIVE, ticket_value= '')
        queue.put(ticket)
        main_window.event_generate("<<CheckQueue>>",  when='tail')
  result = DataFrame(match, columns = column2_list, dtype=object)
  
  queue.put(rejected)
  queue.put(result)

  ticket = Ticket(ticket_type= Ticket_pourpose.END_TASK, ticket_value= '')
  queue.put(ticket)
  main_window.event_generate("<<CheckQueue>>",  when='tail')
