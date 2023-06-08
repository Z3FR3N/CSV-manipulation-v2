from functions.Function import Function, MainWindow
import numpy as np
import datetime as dt
from multiprocessing.pool import ThreadPool

# functions contiene le funzioni che manipolano i dati

class ColumnsComparison(Function):
    def __init__(self, main_window : MainWindow):
        super().__init__('Comparazione colonne e prelievo', main_window, 100, 200)
        self.focus()
        print('Instanziata')

    def generate(self):
      print('do something')

class Banana(Function):
  def __init__(self, main_window : MainWindow):
    super().__init__('Comparazione colonne e prelievo', main_window, 100, 200)
    self.focus()

  def generate(self):
    print('do something')

""" '
def carica_file(numero):
        root = tk.Tk()
        # Hide the window
        root.attributes('-alpha', 0.0)
        # Always have it on top
        root.attributes('-topmost', True)
        percorso = filedialog.askopenfilename(parent= root, title="Seleziona " + 
                                              numero + " file", 
                                              filetypes=(("File csv", "*.csv"), 
                                                         ("Tutti i file", "*.*")))
        root.destroy()
        return percorso

def preleva_separatore(file):
        nome_file = str(file).rpartition("/")[2]
        separatore = input("Indica il separatore per \"" + 
                           str(nome_file) + "\"\n> ")
        return separatore

def leggi_csv(file, separatore):
        elenco = pd.read_csv(file, 
                             index_col=0, 
                             sep=str(separatore), 
                             dtype=str, 
                             low_memory=False)
        return elenco

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