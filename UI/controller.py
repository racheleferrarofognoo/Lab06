from UI.view import View #import sia la view sia il model
from model.model import Autonoleggio #questo è il model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view : View, model : Autonoleggio):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler

    def mostra_automobili(self, e):
        #PULSANTE MOSTRA
        #prende tutte le auto dal model e aggiorna la view.
         #gestisce i tre casi
        #1 result is none = errore nel database
        #2 lista vuota = nessuna auto
        #3 altrimenti popolo la listview


        result = self._model.get_automobili()

        if result is None:
            # errore nel model/DB
            self._view.show_alert("Errore durante la lettura delle automobili dal database.")
            self._view.svuota_lista_auto() #svuoto che è nel view
            return

        if len(result) == 0:
            # nessuna automobile presente nel DB
            self._view.svuota_lista_auto()
            self._view.show_alert("Nessuna automobile trovata.")
            return

        # altrimenti popoliamo la listview
        self._view.popola_lista_auto(result)

    def cerca_automobili(self, e):
        #PULSANTE CERCA
        #legge il modello dalla view, chiama il model e aggiorna la view.

        modello = (self._view.input_modello_auto.value or "").strip() #nella view prendo il valore del textfield
        if modello == "":
            self._view.show_alert("Inserisci il modello da cercare.")
            return

        result = self._model.cerca_automobili_per_modello(modello)

        if result is None:
            # errore DB
            self._view.show_alert("Errore durante la ricerca nel database.")
            self._view.svuota_lista_ricerca()
            return

        if len(result) == 0:
            # nessun risultato per quel modello
            self._view.svuota_lista_ricerca()
            self._view.show_alert(f"Nessuna automobile trovata per il modello {modello}")
            return

        # mostra risultati
        self._view.popola_lista_auto_ricerca(result)
        self._view.update()


