import mysql.connector
from database.DB_connect import get_connection
from model.automobile import Automobile

'''
    MODELLO: 
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Autonoleggio:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_automobili(self) -> list[Automobile] | None:
        """
            Funzione che legge tutte le automobili nel database
            :return: una lista con tutte le automobili presenti oppure None
        """
        conn = None
        try:
            conn = get_connection()#stabilisco connessione col database chiamando la funzione get_connection
            cursor = conn.cursor()
            query = """SELECT * FROM automobile"""
            cursor.execute(query)
            risultati = cursor.fetchall() #acquisisci tutti i risultati presenti nel database

            automobili = []
            for riga in risultati:
                codice = riga[0]
                marca = riga[1]
                modello = riga[2]
                anno = riga[3]
                posti = riga[4]
                disponibile = bool(riga[5])  # 1 True, 0 False

                auto = Automobile(codice, marca, modello, anno, posti, disponibile)
                automobili.append(auto)

            return automobili
        except mysql.connector.Error as err:
            print("Errore in get_automobili")
            return None
        finally:
            if conn:
                conn.close()


    def cerca_automobili_per_modello(self, modello) -> list[Automobile] | None:
        """
            Funzione che recupera una lista con tutte le automobili presenti nel database di una certa marca e modello
            :param modello: il modello dell'automobile
            :return: una lista con tutte le automobili di marca e modello indicato oppure None
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """SELECT * FROM automobile """
             # il modello deve essere una tupla o una lista
            cursor.execute(query)
            risultati = cursor.fetchall()

            automobili = []
            for riga in risultati:
                codice = riga[0]
                marca = riga[1]
                modello_auto = riga[2]
                anno = riga[3]
                posti = riga[4]
                disponibile = bool(riga[5])


                if modello_auto == modello:
                    automobili.append(Automobile(codice, marca, modello, anno, posti, disponibile))#aggiungo alla lista solo le auto di quel modello

            return automobili
        except mysql.connector.Error as err:
            print("Errore in cerca_automobili_per_modello")
            return None
        finally:
            if conn:
                conn.close()