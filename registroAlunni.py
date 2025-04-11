import DBconnection

# Nome del database
dbName = "StudentsRegister"

def create():
    """Crea le tabelle necessarie nel database se non esistono già"""
    conn = DBconnection.db_connection(dbName)  # Connessione al database
    cursor = conn.cursor()

    # Crea tabella studenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS studenti (
        id INT AUTO_INCREMENT PRIMARY KEY,  # ID univoco per ogni studente
        nome VARCHAR(255),  # Nome dello studente
        cognome VARCHAR(255)  # Cognome dello studente
    )
    """)

    # Crea tabella voti con relazione foreign key
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voti (
        id INT AUTO_INCREMENT PRIMARY KEY,  # ID univoco per ogni voto
        studente_id INT,  # ID dello studente a cui appartiene il voto
        materia VARCHAR(255),  # Materia del voto
        voto FLOAT,  # Valore del voto
        FOREIGN KEY (studente_id) REFERENCES studenti(id) ON DELETE CASCADE  # Relazione con la tabella studenti
    )
    """)

    conn.commit()  # Salva le modifiche nel database
    cursor.close()  # Chiude il cursore
    conn.close()  # Chiude la connessione
  
class Student():
    """Classe che rappresenta uno studente con i suoi voti"""
    
    def __init__(self, name, surname, id=None):
        self.id = id  # ID dello studente
        self.name = name  # Nome dello studente
        self.surname = surname  # Cognome dello studente
        self.votes = self.load_votes()  # Carica i voti dello studente dal database

    def load_votes(self):
        """Carica i voti dello studente dal database"""
        conn = DBconnection.db_connection(dbName)  # Connessione al database
        cursor = conn.cursor()
        cursor.execute("SELECT materia, voto FROM voti WHERE studente_id = %s", (self.id,))  # Query per ottenere i voti
        results = cursor.fetchall()  # Ottiene tutti i risultati
        conn.close()  # Chiude la connessione

        # Organizza i voti per materia
        votes = {}
        for materia, voto in results:
            if materia not in votes:
                votes[materia] = []  # Inizializza la lista dei voti per la materia
            votes[materia].append(voto)  # Aggiunge il voto alla lista
        return votes

    def exist_valutation(self, materia):
        """Verifica se esiste almeno un voto per la materia specificata"""
        return materia in self.votes  # Controlla se la materia è presente nei voti

    def add_all_valutation(self):
        """Aggiunge voti per tutte le materie principali"""
        subjects = ['Matematica', 'Italiano', 'Inglese', 'Storia']  # Elenco delle materie principali
        conn = DBconnection.db_connection(dbName)  # Connessione al database
        cursor = conn.cursor()
        
        for materia in subjects:
            voto = float(input(f"Inserisci voto per {materia}: "))  # Richiede il voto per la materia
            cursor.execute("""
                INSERT INTO voti (studente_id, materia, voto) 
                VALUES (%s, %s, %s)
            """, (self.id, materia, voto))  # Inserisce il voto nel database
            
        conn.commit()  # Salva le modifiche
        conn.close()  # Chiude la connessione
        self.votes = self.load_votes()  # Ricarica i voti aggiornati

    def add_one_valutation(self):
        """Aggiunge un singolo voto per una materia specifica"""
        materia = input("Inserisci materia: ").strip()  # Richiede la materia
        voto = float(input(f"Inserisci voto per {materia}: "))  # Richiede il voto
        
        conn = DBconnection.db_connection(dbName)  # Connessione al database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO voti (studente_id, materia, voto) 
            VALUES (%s, %s, %s)
        """, (self.id, materia, voto))  # Inserisce il voto nel database
        
        conn.commit()  # Salva le modifiche
        conn.close()  # Chiude la connessione
        self.votes = self.load_votes()  # Ricarica i voti aggiornati

    def print_info(self):
        """Stampa le informazioni complete dello studente"""
        print(f"\nID: {self.id} Studente: {self.name} {self.surname}")  # Stampa ID, nome e cognome
        
        for materia, voti in self.votes.items():
            media = sum(voti) / len(voti)  # Calcola la media dei voti per la materia
            print(f"Materia: {materia}, Voti: {voti}, Media: {round(media, 2)}")  # Stampa i dettagli della materia
            
        print(f"Media generale: {self.med_all_vote()}\n")  # Stampa la media generale

    def print_subject(self):
        """Stampa l'elenco delle materie dello studente"""
        print("Materie:", ", ".join(self.votes.keys()))  # Stampa tutte le materie

    def med_vote_for_subject(self, materia):
        """Calcola la media per una specifica materia"""
        if materia in self.votes:
            return round(sum(self.votes[materia]) / len(self.votes[materia]), 2)  # Calcola la media
        return 0  # Ritorna 0 se la materia non ha voti

    def med_all_vote(self):
        """Calcola la media generale di tutti i voti"""
        total = count = 0
        for voti in self.votes.values():
            total += sum(voti)  # Somma tutti i voti
            count += len(voti)  # Conta il numero totale di voti
        return round(total / count, 2) if count > 0 else 0  # Calcola la media generale o ritorna 0 se non ci sono voti


class Register():
    """Classe che gestisce il registro degli studenti"""
    
    def __init__(self):
        self.student = self.load_all_students()  # Carica tutti gli studenti

    def load_all_students(self):
        """Carica tutti gli studenti dal database"""
        conn = DBconnection.db_connection(dbName)  # Connessione al database
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cognome FROM studenti")  # Query per ottenere gli studenti
        results = cursor.fetchall()  # Ottiene tutti i risultati
        conn.close()  # Chiude la connessione

        studenti = {}
        for student_id, nome, cognome in results:
            studente = Student(nome, cognome, student_id)  # Crea un'istanza di Student
            studenti[student_id] = studente  # Aggiunge lo studente al dizionario
        return studenti

    def add_student(self):
        """Aggiunge un nuovo studente al registro"""
        nome = input("Nome: ").strip()  # Richiede il nome
        cognome = input("Cognome: ").strip()  # Richiede il cognome

        # Controllo duplicati
        for studente in self.student.values():
            if studente.name == nome and studente.surname == cognome:
                print("Studente già presente!")  # Messaggio di errore
                return

        conn = DBconnection.db_connection(dbName)  # Connessione al database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO studenti (nome, cognome) 
            VALUES (%s, %s)
        """, (nome, cognome))  # Inserisce lo studente nel database
        
        conn.commit()  # Salva le modifiche
        student_id = cursor.lastrowid  # Ottiene l'ID dell'ultimo studente inserito
        conn.close()  # Chiude la connessione

        nuovo = Student(nome, cognome, student_id)  # Crea un'istanza di Student
        self.student[student_id] = nuovo  # Aggiunge lo studente al dizionario
        print("Studente aggiunto con successo!\n")  # Messaggio di conferma

    def delete_student(self):
        """Elimina uno studente dal registro"""
        student_id = int(input("Inserisci l'ID dello studente da eliminare: "))  # Richiede l'ID dello studente

        if student_id not in self.student:
            print("Studente non presente.")  # Messaggio di errore
            return

        try:
            conn = DBconnection.db_connection(dbName)  # Connessione al database
            cursor = conn.cursor()

            cursor.execute("DELETE FROM studenti WHERE id = %s", (student_id,))  # Elimina lo studente dal database
            conn.commit()  # Salva le modifiche

            # Rimuovilo anche dal dizionario interno
            del self.student[student_id]  # Rimuove lo studente dal dizionario

            print(f"Studente con ID {student_id} eliminato correttamente.")  # Messaggio di conferma

        except Exception as e:
            print("Errore durante l'eliminazione:", e)  # Messaggio di errore

        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione
                
    def modify_student_vote(self):
        """Modifica un voto specifico per uno studente"""

        student_id = int(input("Inserisci l'ID dello studente: "))  # Richiede l'ID dello studente

        if student_id not in self.student:
            print("Studente non presente.")  # Messaggio di errore
            return

        materia = input("Inserisci la materia del voto da modificare: ").strip()  # Richiede la materia

        try:
            conn = DBconnection.db_connection(dbName)  # Connessione al database
            cursor = conn.cursor()

            # Recupera i voti per la materia specifica
            cursor.execute("""
                SELECT id, voto FROM voti
                WHERE studente_id = %s AND materia = %s
            """, (student_id, materia))  # Query per ottenere i voti
            voti = cursor.fetchall()  # Ottiene tutti i risultati

            if not voti:
                print(f"Nessun voto trovato per la materia {materia}.")  # Messaggio di errore
                return

            print(f"Voti trovati per {materia}:")  # Stampa i voti trovati
            for voto_id, voto in voti:
                print(f"ID Voto: {voto_id} - Voto: {voto}")  # Stampa i dettagli del voto

            voto_id_modifica = int(input("Inserisci l'ID del voto da modificare: "))  # Richiede l'ID del voto
            nuovo_voto = float(input("Inserisci il nuovo voto: "))  # Richiede il nuovo voto

            # Modifica il voto selezionato
            cursor.execute("""
                UPDATE voti
                SET voto = %s
                WHERE id = %s AND studente_id = %s
            """, (nuovo_voto, voto_id_modifica, student_id))  # Aggiorna il voto nel database

            conn.commit()  # Salva le modifiche
            print(f"Voto con ID {voto_id_modifica} aggiornato a {nuovo_voto}.")  # Messaggio di conferma

            # Aggiorna i voti anche nel dizionario in memoria
            self.student[student_id].votes = self.student[student_id].load_votes()  # Ricarica i voti aggiornati

        except Exception as e:
            print("Errore durante la modifica del voto:", e)  # Messaggio di errore

        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione
                
    def modify_student(self):
        """Modifica nome e cognome di uno studente"""

        student_id = int(input("Inserisci l'ID dello studente da modificare: "))  # Richiede l'ID dello studente

        if student_id not in self.student:
            print("Studente non presente.")  # Messaggio di errore
            return

        nuovo_nome = input("Inserisci il nuovo nome: ").strip()  # Richiede il nuovo nome
        nuovo_cognome = input("Inserisci il nuovo cognome: ").strip()  # Richiede il nuovo cognome

        try:
            conn = DBconnection.db_connection(dbName)  # Connessione al database
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE studenti
                SET nome = %s, cognome = %s
                WHERE id = %s
            """, (nuovo_nome, nuovo_cognome, student_id))  # Aggiorna nome e cognome nel database
            conn.commit()  # Salva le modifiche

            # Aggiorna anche il dizionario in memoria
            self.student[student_id].name = nuovo_nome  # Aggiorna il nome
            self.student[student_id].surname = nuovo_cognome  # Aggiorna il cognome

            print(f"Studente con ID {student_id} modificato correttamente.")  # Messaggio di conferma

        except Exception as e:
            print("Errore durante la modifica:", e)  # Messaggio di errore

        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione

    def print_all_student(self):
        """Stampa le informazioni di tutti gli studenti nel registro"""
        for studente in self.student.values():
            studente.print_info()  # Stampa le informazioni dello studente


def main():
    """Funzione principale che gestisce il menu"""
    register = Register()  # Crea un'istanza di Register

    while True:
        try:
            ch = int(input(
                "\n--- Menu ---\n"
                " 1) Visualizza studenti\n"
                " 2) Aggiungi studente\n"
                " 3) Aggiungi tutti i voti a uno studente\n"
                " 4) Aggiungi voto singolo a uno studente\n"
                " 5) Elimina studente\n"
                " 6) Modifica nome/cognome studente\n"
                " 7) Modifica voto\n"
                " 8) Esci\n"
                " ---> "
            ))  # Richiede la scelta dell'utente
        except ValueError:
            print("Inserisci un numero valido.")  # Messaggio di errore
            continue

        match ch:
            case 1:
                register.print_all_student()  # Visualizza tutti gli studenti
            case 2:
                register.add_student()  # Aggiunge un nuovo studente
            case 3:
                stud_id = int(input("Inserisci l'ID dello studente: "))  # Richiede l'ID dello studente
                if stud_id in register.student:
                    register.student[stud_id].add_all_valutation()  # Aggiunge tutti i voti
                else:
                    print("Studente non trovato.")  # Messaggio di errore
            case 4:
                stud_id = int(input("Inserisci l'ID dello studente: "))  # Richiede l'ID dello studente
                if stud_id in register.student:
                    register.student[stud_id].add_one_valutation()  # Aggiunge un voto singolo
                else:
                    print("Studente non trovato.")  # Messaggio di errore
            case 5:
                register.delete_student()  # Elimina uno studente
            case 6:
                register.modify_student()  # Modifica nome e cognome di uno studente
            case 7:
                register.modify_student_vote()  # Modifica un voto
            case 8:
                print("Uscita dal programma...")  # Messaggio di uscita
                break
            case _:
                print("Scelta non valida.")  # Messaggio di errore

        if input("Vuoi tornare al menu? (s/n) ---> ").strip().lower() == "n":  # Richiede se tornare al menu
            break


# Crea le tabelle e avvia il programma
create()  # Crea le tabelle nel database
main()  # Avvia il programma