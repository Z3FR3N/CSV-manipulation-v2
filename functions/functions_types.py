from functions.function import Function, main
from tkinter import StringVar, IntVar, Canvas
from tkinter.ttk import Combobox, Frame, Label, Separator, Button, Checkbutton, Scrollbar
from tkinter.constants import NSEW, EW
from dialogs.dialogs import Parameters, Error, ScrollableFrame
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

    self.main_frame = Frame(self._window.content) # to allocate a label and a Combobox
    self.main_frame.grid_columnconfigure(0, weight=1)
    self.main_frame.grid_rowconfigure(0, weight=4)
    self.main_frame.grid_rowconfigure(1, weight=4)
    self.main_frame.grid_rowconfigure(2, weight=1)
    self.main_frame.grid(column=0, row=0, sticky='NSEW')
    
    self.top_frame = Frame(self.main_frame)
    self.top_frame.grid(column= 0, row= 0)

    self.csv_label = Label(self.top_frame, text= 'CSV: ')
    self.csv_label.grid(column=0, row=0)

    self.choices = Combobox( self.top_frame, 
                              textvariable= self._selected_csv,
                              values= csv_available)
        
    self.choices.grid(column= 1, row=0)

    self.csv_button = Button(self.top_frame, text='Leggi', command= self.read)
    self.csv_button.grid(column=2, row= 0, padx= 5, pady= 5)

    # Adding a separator

    self.separatore = Separator(self.main_frame, orient='horizontal')
    self.separatore.grid(column=0, row=1, sticky='EW')
   
    # Il secondo cambia la vista in base ai valori
    self.bottom_frame = Frame(self.main_frame)
    self.bottom_frame.grid_columnconfigure(0, weight=1, minsize=300)
    self.bottom_frame.grid_rowconfigure(0, weight= 1)
    self._window.update_idletasks()
    self.scrollable = ScrollableFrame(self.bottom_frame, (self._window.winfo_reqheight() - self.top_frame.winfo_reqheight() - self._window.bottom_frame.winfo_reqheight()))

    self.scrollable.grid(column= 0, row=0, sticky=NSEW)
    self.bottom_frame.grid(column=0, row=2, sticky=EW)
    
  def read(self):
    # Prelevo il Dataframe
    try:
      csv = self._selected_csv.get()
      self._columns_list = DataFrame(self._data_map[csv]).columns.values.tolist()
    except:
      Error(self.main_window, 'Qualcosa è andato storto')
    
    # Create a list of IntVar as big as column_list
    self._chosen = []
    for name in self._columns_list:
      self._chosen.append(IntVar().set(1))

    # Counter
    grid_row = 0
    self._window.update_idletasks()
    for i in range(len(self._chosen)):
      check = Checkbutton(self.scrollable.interior, text = self._columns_list[i], variable = self._chosen[i])
      check.grid(column= 0, row= grid_row, padx= (((self._window.winfo_reqwidth() - check.winfo_reqwidth() - self.scrollable.vscrollbar.winfo_reqwidth()) / 2)))
      grid_row+= 1

    # Passo a generate
    
  def generate(self, csv: DataFrame, colums : list):
    # Ritaglio il Dataframe e ne restituisco uno risultante
    print('do something')

  def export(self):
    # Passo il Dataframe a Table
    return super().export()
  
  def info(self):
    return super().info()

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