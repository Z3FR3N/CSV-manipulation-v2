# Implementazione

![wireframe](./wireframing/wireframing.svg)

E' opportuno trovare gli elementi corretti del package Tkinter per rappresentare correttamente le varie finestre presenti:

1. Finestra principale
2. Fin. di caricamento
3. Fin. di informazioni
4. Fin. per i parametri
5. Fin. di attesa
6. Fin. di salvataggio

La finestra principale verrà inizializzata dall'interprete tramite `tk.Tk()` e per gestire la gerarchia delle finestre verrà utilizzata la classe `Toplevel()`. Gli elementi delle finestre, come bottoni, pulsanti di controllo e liste vengono identificati dal modulo Tkinter come *widgets*. Buona prassi nell'utilizzo di Tkinter è l'utilizzo del widgets [`Frame()`](http://tkdocs.com/widgets/frame.html) per "contenerne" altri.

### Finestra principale - `Window()`

La finestra più ricca di elementi è la finestra principale(da quì il suo ruolo). Buona prassi è far ospitare da un `Frame()` padre la disposizione interna degli elementi. Il resizing viene gestito attraverso i metodi `columnconfigure` e `rowconfigure`.

### Griglia - `Grid()`

Occorre configurare la griglia di appoggio ai vari widgets: deve essere 4X7 potrebbe essere adatta. Non raggiunge le dimensioni settate fino a che non viene popolata di elementi, tramite `columnspan` e `rowspan` è possibile far coprire più righe/colonne agli elementi.

### Bottoni - `Button()`

- *Opzioni*: Non ancora utilizzato, utile in caso di implementazione di un API per le funzioni personalizzate
- *Info*: Apre la finestra di spiegazione delle funzioni
- *Genera*: Lancia la funzione selezionata, generando il file di otuput
- *Carica*: Caricamento dei file CSV, chiaramente viene prima caricato il primo file e poi il secondo
- *Reset*: Riporta la finestra allo stato iniziale eliminando i progressi
- *Salva*: Permette di salvare i file
- *Inverti*: Inverte i csv caricati(l'ordine può essere utile in determinate funzioni)

### Preview CSV - `Notebook()`

Rappresenta l'anteprima di *n* righe del file caricato e può essere utile anche per una "copia al volo" di alcuni dati. *Non si presuppone* la modifica o l'utilizzo delle colonne in maniera massiva che va fatta attraverso l'uso delle funzioni.

### Lista funzioni - `Combobox()`

Combobox che contiene la lista delle delle funzioni disponibili, eredita 

### Finestra di attesa - `ProgressBar()`

Comunica all'utente l'avanzamento dell'elaborazione. *Attualmente non funzionante* per un thread lock causato dal Dataframe che impedisce a Tkinter di gestire la UI. Refactoring necessario.

<<<<<<< HEAD
### Demo
[![Video demo](video/thumbnail.png)](video/demo.mp4)

=======
>>>>>>> 9b0e8a4 (demo video not working)
