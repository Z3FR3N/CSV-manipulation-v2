from functions.function import Function, main
from tkinter import StringVar, IntVar, Canvas
from tkinter.ttk import Combobox, Frame, Label, Separator, Button, Checkbutton, Scrollbar
<<<<<<< HEAD
from tkinter.constants import *
=======
>>>>>>> 0acbba1 (updated function_types)
from dialogs.dialogs import Parameters, Error
from pandas import DataFrame
import numpy as np
import datetime as dt
from multiprocessing.pool import ThreadPool

# functions_types contains every data-manipulating class
# We need to use the data getters every time we need data -> Dataframes are not memory safe.
# TODO: -Create an API to dinamically import functions from files in a folder
#       -Return a Dataframe with missing/errors

class Multiplesearch(Function):
# restituire un dataframe con le voci scartate
    def __init__(self, main_window : main):
      super().__init__('Ricerca multipla', main_window)
    
    def take_parameters(self):
      print(self.name)
      super().take_parameters()
      # TODO: prelevare l'header, selezionare le colonne chiave

    def generate(self):
      # TODO: Filtrare le colonne chiave, generare il DataFrame utilizzando Loading
      print('do something')

    def export(self):
      # TODO: Utilizzare Columnsselection per scegliere le colonne
      return super().export()

    def info(self):
      return super().info()

class Columnsselection(Function, Parameters):
  def __init__(self, main_window : main):
    super().__init__('Selezione colonne', main_window)

  def take_parameters(self):
    super().take_parameters()
    # self._data1 
    # self._data2 
    # self._first_file_name
    # self._second_file_name
    # self._window

    # Popolo una lista di candidati che comprenda CSV di input e risultati
    csv_available = list()
    csv_available.append(self._first_file_name)
    csv_available.append(self._second_file_name)
    csv_available.extend(self.main_window.results_names)

    data_available = list()
    data_available.append(self._data1)
    data_available.append(self._data2)
    data_available.extend(self.main_window._results)

    self._data_map = dict(zip(csv_available, data_available))

    # Variabile che indica la scelta
    self._selected_csv = StringVar()

<<<<<<< HEAD
    self._main_frame = Frame(self._window.content) # to allocate a label and a Combobox
    self._main_frame.grid(column=0, row=0, sticky='NSEW', pady=3)
    self._main_frame.grid_columnconfigure(0, weight=1)
    self._main_frame.grid_rowconfigure(0, weight=1)
    self._main_frame.grid_rowconfigure(1, weight=1)
    self._main_frame.grid_rowconfigure(2, weight=2, minsize=230)
    
    self._top_frame = Frame(self._main_frame)
    self._top_frame.grid(column= 0, row= 0)

    self._csv_label = Label(self._top_frame, text= 'CSV: ')
    self._csv_label.grid(column=0, row=0)

    self._choices = Combobox( self._top_frame, 
                              textvariable= self._selected_csv,
                              values= csv_available)
        
    self._choices.grid(column= 1, row=0)

    self._csv_button = Button(self._top_frame, text='Leggi', command= self.read)
    self._csv_button.grid(column=2, row= 0, padx= 5, pady= 5)

    # Adding a separator

    self._separatore = Separator(self._main_frame, orient='horizontal')
    self._separatore.grid(column=0, row=1, sticky='EW')
   
    # Il secondo cambia la vista in base ai valori
    self._bottom_frame = (self._main_frame)
    self._bottom_frame.grid_columnconfigure(0,weight=1)

    ## Initialize canvas and scrollbar
    #self._scrollbar = Scrollbar(self._bottom_frame, orient= 'vertical')
    #self._canvas = Canvas(self._bottom_frame, background='red',width=100, height=100, highlightthickness=0, yscrollcommand=self._scrollbar.set)
    #self._content = Frame(self._canvas)
    #
    ## Configuro il Canvas
    #self._canvas.configure(scrollregion= self._content)
    #self._canvas.configure(yscrollcommand= self._scrollbar.set)
    #self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
    #self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    ## Aggiungo contenuto all'interno di una finestra del canvas
    #self._canvas.create_window((0,0), window=self._content, anchor='nw')
    ## Creo un frame interno al Canvas
    #self._scrollbar.grid(row=0, column= 1, sticky='NS')
    #self._canvas.grid(column=0, row=0)

    self._frame = ScrollableFrame(self._bottom_frame)
    self._bottom_frame.grid(row=2, column=0, sticky= NSEW)
    self._frame.grid(column=0, row=0, sticky=NSEW)
    self._main_frame.update()
    self._main_frame.update_idletasks()

    for i in range(100):
      Button(self._frame.interior, text=f"Button {i}").grid(column=0, row=i)

=======
    top_frame = Frame(self._window.content) # to allocate a label and a Combobox
    top_frame.grid(column=0, row=0, sticky='NSEW')
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_rowconfigure(0, weight=1)
    
    
    bottom_frame = Frame
    
    inner_top_frame = Frame(top_frame)
    inner_top_frame.grid()

    csv_label = Label(inner_top_frame, text= 'CSV: ')
    csv_label.grid(column=0, row=0)

    choices = Combobox( inner_top_frame, 
                        textvariable= self._selected_csv,
                        values= csv_available)
        
    choices.grid(column= 1, row=0)
#
    #csv_button = Button(inner_top_frame, text='leggi', command= self.read)
    #csv_button.grid(column=2, row= 0, padx= 5, pady= 5)
#
    ## Adding a separator
#
    #separatore = Separator(self._window.content, orient='horizontal')
    #separatore.grid(column=0, row=1, sticky='EW', pady=4)
#
    ## Il secondo cambia la vista in base ai valori
    #self._bottom_frame = (self._window.content)
    #self._bottom_frame.grid(row=2, column=0, sticky='EW')


>>>>>>> 0acbba1 (updated function_types)
  def read(self):
    # Prelevo il Dataframe
    try:
      csv = self._selected_csv.get()
      self._columns_list = DataFrame(self._data_map[csv]).columns.values.tolist()
    except:
      Error(self.main_window, 'Qualcosa è andato storto')
<<<<<<< HEAD
=======

    self._canvas = Canvas(self._bottom_frame, width=(278), highlightthickness=0)
    self._canvas.grid(column=0, row=0, sticky='NSEW')
    self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # Creo una scrollbar per il Canvas
    scrollbar = Scrollbar(self._bottom_frame, orient= 'vertical', command= self._canvas.yview)
    scrollbar.grid(row=0, column= 1, sticky='NS')

    # Configuro il Canvas
    self._canvas.configure(yscrollcommand=scrollbar.set)
    self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

    # Creo un frame interno al Canvas
    content = Frame(self._canvas)
    content.rowconfigure(0, weight=2)
    content.columnconfigure(0, weight=2)

    # Aggiungo contenuto all'interno di una finestra del canvas
    self._canvas.create_window((0,0), window=content, anchor='nw')
>>>>>>> 0acbba1 (updated function_types)
    
    # Create a list of IntVar as big as column_list
    self._chosen = []
    for name in self._columns_list:
      self._chosen.append(IntVar().set(1))

    # Counter
    grid_row = 0

    for i in range(len(self._chosen)):
<<<<<<< HEAD
      check = Checkbutton(self._frame.scrollable_frame, text = self._columns_list[i], variable = self._chosen[i], onvalue=IntVar(self._chosen[i]).get())
      check.grid(column= 0, row= grid_row)
      grid_row+= 1

    self._canvas.update_idletasks()
=======
      check = Checkbutton(content, text = self._columns_list[i], variable = self._chosen[i], onvalue=IntVar(self._chosen[i]).get())
      check.grid(column= 0, row= grid_row)
      grid_row+= 1
    
    
    
>>>>>>> 0acbba1 (updated function_types)
    # Visualizzo le colonne da esportare

    # Passo a generate
    
  def generate(self, csv: DataFrame, colums : list):
    # Ritaglio il Dataframe e ne restituisco uno risultante
    print('do something')

  def export(self):
    # Passo il Dataframe a Table
    return super().export()
  
  def info(self):
    return super().info()
  
  def _on_mousewheel(self, event):
      self._canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class ScrollableFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.grid(column=1, row=0, sticky=NS)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, 
                                width = 300, height = 100,
                                yscrollcommand=vscrollbar.set)
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        vscrollbar.config(command = self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
        
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
    
    def _on_mousewheel(self, event):
      self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

"""
def leggi_header(elenco: pd.DataFrame):
        lista_colonne = elenco.columns.values.tolist()
        numero_colonne = np.size(lista_colonne)
        nomi_colonne = str()
        j = 1
        for i in lista_colonne:
                nomi_colonne += str(j) + " >> " + i + "\n"
                j += 1
        return nomi_colonne, str(numero_colonne)

def filtra(prima_colonna_chiave: str, 
           seconda_colonna_chiave: str, 
           primo_elenco: pd.DataFrame, 
           secondo_elenco: pd.DataFrame):
        prima_colonna_chiave = int(prima_colonna_chiave) - 1
        seconda_colonna_chiave = int(seconda_colonna_chiave) - 1
        prima_lista_colonne = primo_elenco.columns.values.tolist()
        seconda_lista_colonne = secondo_elenco.columns.values.tolist()
        nome_prima_colonna_chiave = prima_lista_colonne[prima_colonna_chiave]
        nome_seconda_colonna_chiave = seconda_lista_colonne[seconda_colonna_chiave]
        print("Le colonne-chiavi selezionate sono: "    + nome_prima_colonna_chiave 
                                                        + " e " + nome_seconda_colonna_chiave)
        #DTP -> Dato non presente
        primo_elenco = primo_elenco.to_numpy(na_value="DTP", dtype=pd.StringDtype)
        secondo_elenco = secondo_elenco.to_numpy(na_value="DNP", dtype=pd.StringDtype)
        lista_finale = []
        lista_scartati = []
        # con il threading possiamo velocizzare i confronti, ma occorre riordinare la lista 
        # o il dataframe uscente in base al tipo di dato
        def task():
                for riga in primo_elenco:
                        cod_fiscale1 = riga[prima_colonna_chiave]
                        lista_scartati.append(cod_fiscale1)
                        for riga2 in secondo_elenco:
                                cod_fiscale2 = riga2[seconda_colonna_chiave]
                                if str(cod_fiscale1) == str(cod_fiscale2):
                                        lista_finale.append(riga2)
                                        lista_scartati.remove(cod_fiscale1)
        # create and configure the thread pool
        with ThreadPool() as pool:
                # issue tasks to the thread pool
                result = pool.apply_async(task)
                # wait for the result
                result.wait()
        elenco_finale = pd.DataFrame(lista_finale, columns = seconda_lista_colonne, dtype=object)
        return elenco_finale, lista_scartati

def colonne_da_tenere(elenco: pd.DataFrame):
        colonne_disponibili = elenco.columns.values.tolist()
        nomi_colonne = leggi_header(elenco)[0]
        print("\nSono disponibli le seguenti colonne:\n\n" + nomi_colonne)
        colonne_tenute = input("Quali colonne tenere? Indicare il numero separato da una virgola." +
                               "\n(Premere invio per mantenerle tutte)\n> ")
        if colonne_tenute == "":
                return colonne_disponibili
        else:
                colonne_scelte = colonne_tenute.split(",")
        nome_colonne_scelte = []
        for col in colonne_scelte:
                col = col.strip()
                nome_colonne_scelte.append(str(colonne_disponibili[int(col) - 1]))
        return nome_colonne_scelte

def rimuovi_colonne(nomi_colonne:list[str], elenco:pd.DataFrame):
        colonne_elenco = elenco.columns.values.tolist()
        colonne_da_rimuovere = set(colonne_elenco).difference(set(nomi_colonne))
        elenco.drop(columns=list(colonne_da_rimuovere), inplace= True)
        
def salva_file(data: pd.DataFrame, lista_scartati:list[str], separatore:str ):
        root = tk.Tk()
        # Hide the window
        root.attributes('-alpha', 0.0)
        # Always have it on top
        root.attributes('-topmost', True)
        percorso = filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("File csv","*.csv")])
        data.to_csv(percorso, index=False, lineterminator='\n', encoding='utf-8', sep=separatore)
        # Open our existing CSV file in append mode
        # Create a file object for this file
        root.destroy()
        # Mettere un controllo:
        #       Se il file esiste -> Aggiunge al file
        #       Se il file non esiste -> Crea il file
        with open('Scartati al '+ str(dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + '.txt', 'w') as f:
                f.write('Codici senza corrispondenza:\n'.join(lista_scartati))
        dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# Not useful ma ormai l'ho scritta
def modifica_colonne(elenco: pd.DataFrame):
        print("\n" + leggi_header(elenco)[0])
        lista_colonne_disponibili = elenco.columns.values.tolist()
        print('Vuoi convertire dei valori in numeri interi?')
        while (True):
                risposta = input('Rispondi con \'si\' o \'no\':\n>')
                if (risposta.lower() == "si" or risposta.lower() == "sì"):
                        print("Quali colonne modificare?")
                        colonne_da_modificare = input("Indica il numero separato da una virgola.\n> ")
                        if colonne_da_modificare == "":
                                break
                        else:
                                lista_colonne_da_modificare = colonne_da_modificare.split(",")
                                nome_colonne_scelte = []
                                for col in lista_colonne_da_modificare:
                                        col = col.strip()
                                        nome_colonne_scelte.append(str(lista_colonne_disponibili[int(col) - 1]))
                                        # convert column "a" of a DataFrame
                                        for nome in nome_colonne_scelte:
                                                elenco[nome] = pd.to_numeric(elenco[nome], downcast='integer')
                        return elenco
                if risposta.lower() == "no":
                        break
        return elenco """