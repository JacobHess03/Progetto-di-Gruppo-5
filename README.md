# Registro Studenti 📚

Un'applicazione Python per la gestione di un registro studenti con salvataggio persistente tramite database MySQL.

## 🚀 Funzionalità principali

- Aggiunta di studenti con nome e cognome
- Visualizzazione dell'elenco studenti
- Inserimento di voti per materie (Matematica, Italiano, Inglese, Storia)
- Calcolo della media voti per materia e media generale
- Visualizzazione del miglior studente
- Calcolo della media della classe
- Modifica nome e cognome di uno studente
- Modifica di un voto specifico per materia
- Eliminazione di uno studente e dei suoi voti associati

## 🧰 Requisiti

- Python 3.x
- MySQL Server
- Modulo Python `mysql-connector-python`

Installa il pacchetto necessario con:

```bash
pip install mysql-connector-python
```

⚙️ Struttura del progetto
```
    main.py - punto di ingresso principale del programma

    DBconnection.py - modulo per la connessione al database MySQL

    Student - classe che rappresenta uno studente e i suoi voti

    Register - classe per gestire l’intero registro

    create() - funzione che crea le tabelle nel database se non esistono
```
🗃️ Database

Il progetto utilizza un database MySQL denominato StudentsRegister con due tabelle:
```
    studenti: contiene id, nome, cognome

    voti: contiene id, studente_id, materia, voto
```
La relazione è 1:N tra studenti e voti.
🖥️ Avvio

Per eseguire il programma:
```
python main.py
```
Durante l'esecuzione, ti verrà mostrato un menu interattivo:
```
--- Menu ---
 1) Visualizza studenti
 2) Aggiungi studenti
 3) Aggiungi 1 voto per materia a uno studente
 4) Aggiungi voto per specifica materia
 5) Miglior studente
 6) Elimina studente
 7) Modifica studente (nome e cognome)
 8) Media generale della classe
 9) Stampa voti di uno studente
10) Modifica un voto specifico
11) Esci
```
📌 Esempio connessione MySQL

Nel file DBconnection.py, assicurati di avere qualcosa del genere (con i tuoi dati):
```
import mysql.connector

def db_connection(database=None):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="la_tua_password",
        database=database
    )
```
