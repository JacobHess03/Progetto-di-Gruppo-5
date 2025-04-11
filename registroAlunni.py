import DBconnection

# Nome del database
dbName = "StudentsRegister"

def create():
    """Crea le tabelle necessarie nel database se non esistono già"""
    conn = DBconnection.db_connection(dbName)
    cursor = conn.cursor()

    # Crea tabella studenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS studenti (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        cognome VARCHAR(255)
    )
    """)

    # Crea tabella voti con relazione foreign key
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voti (
        id INT AUTO_INCREMENT PRIMARY KEY,
        studente_id INT,
        materia VARCHAR(255),
        voto FLOAT,
        FOREIGN KEY (studente_id) REFERENCES studenti(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
  
class Student():
    """Classe che rappresenta uno studente con i suoi voti"""
    
    def __init__(self, name, surname, id=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.votes = self.load_votes()  # Carica i voti dal database

    def load_votes(self):
        """Carica i voti dello studente dal database"""
        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        cursor.execute("SELECT materia, voto FROM voti WHERE studente_id = %s", (self.id,))
        results = cursor.fetchall()
        conn.close()

        # Organizza i voti per materia
        votes = {}
        for materia, voto in results:
            if materia not in votes:
                votes[materia] = []
            votes[materia].append(voto)
        return votes

    def exist_valutation(self, materia):
        """Verifica se esiste almeno un voto per la materia specificata"""
        return materia in self.votes

    def add_all_valutation(self):
        """Aggiunge voti per tutte le materie principali"""
        subjects = ['Matematica', 'Italiano', 'Inglese', 'Storia']
        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        
        for materia in subjects:
            voto = float(input(f"Inserisci voto per {materia}: "))
            cursor.execute("""
                INSERT INTO voti (studente_id, materia, voto) 
                VALUES (%s, %s, %s)
            """, (self.id, materia, voto))
            
        conn.commit()
        conn.close()
        self.votes = self.load_votes()  # Ricarica i voti aggiornati

    def add_one_valutation(self):
        """Aggiunge un singolo voto per una materia specifica"""
        materia = input("Inserisci materia: ").strip()
        voto = float(input(f"Inserisci voto per {materia}: "))
        
        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO voti (studente_id, materia, voto) 
            VALUES (%s, %s, %s)
        """, (self.id, materia, voto))
        
        conn.commit()
        conn.close()
        self.votes = self.load_votes()  # Ricarica i voti aggiornati

    def print_info(self):
        """Stampa le informazioni complete dello studente"""
        print(f"\nID: {self.id} Studente: {self.name} {self.surname}")
        
        for materia, voti in self.votes.items():
            media = sum(voti) / len(voti)
            print(f"Materia: {materia}, Voti: {voti}, Media: {round(media, 2)}")
            
        print(f"Media generale: {self.med_all_vote()}\n")

    def print_subject(self):
        """Stampa l'elenco delle materie dello studente"""
        print("Materie:", ", ".join(self.votes.keys()))

    def med_vote_for_subject(self, materia):
        """Calcola la media per una specifica materia"""
        if materia in self.votes:
            return round(sum(self.votes[materia]) / len(self.votes[materia]), 2)
        return 0

    def med_all_vote(self):
        """Calcola la media generale di tutti i voti"""
        total = count = 0
        for voti in self.votes.values():
            total += sum(voti)
            count += len(voti)
        return round(total / count, 2) if count > 0 else 0


class Register():
    """Classe che gestisce il registro degli studenti"""
    
    def __init__(self):
        self.student = self.load_all_students()  # Carica tutti gli studenti

    def load_all_students(self):
        """Carica tutti gli studenti dal database"""
        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cognome FROM studenti")
        results = cursor.fetchall()
        conn.close()

        studenti = {}
        for student_id, nome, cognome in results:
            studente = Student(nome, cognome, student_id)
            studenti[student_id] = studente
        return studenti

    def add_student(self):
        """Aggiunge un nuovo studente al registro"""
        nome = input("Nome: ").strip()
        cognome = input("Cognome: ").strip()

        # Controllo duplicati
        for studente in self.student.values():
            if studente.name == nome and studente.surname == cognome:
                print("Studente già presente!")
                return

        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO studenti (nome, cognome) 
            VALUES (%s, %s)
        """, (nome, cognome))
        
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        nuovo = Student(nome, cognome, student_id)
        self.student[student_id] = nuovo
        print("Studente aggiunto con successo!\n")

    def med_of_class(self):
        """Calcola la media generale della classe"""
        total = count = 0
        for studente in self.student.values():
            total += studente.med_all_vote()
            count += 1
            
        if count == 0:
            print("Nessuno studente nel registro.")
        else:
            print(f"Media generale della classe: {round(total / count, 2)}\n")

    def best_student(self):
        """Trova lo studente con la media più alta"""
        best = None
        best_media = -1
        
        for studente in self.student.values():
            media = studente.med_all_vote()
            if media > best_media:
                best = studente
                best_media = media
                
        if best:
            print(f"Miglior studente: {best.name} {best.surname} con media {best_media}\n")
        else:
            print("Nessuno studente disponibile.\n")
    
    def delete_student(self):
        """Elimina uno studente dal registro"""
        student_id = int(input("Inserisci l'ID dello studente da eliminare: "))

        if student_id not in self.student:
            print("Studente non presente.")
            return

        try:
            conn = DBconnection.db_connection(dbName)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM studenti WHERE id = %s", (student_id,))
            conn.commit()

            # Rimuovilo anche dal dizionario interno
            del self.student[student_id]

            print(f"Studente con ID {student_id} eliminato correttamente.")

        except Exception as e:
            print("Errore durante l'eliminazione:", e)

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
      
    def print_all_student(self):
        """Stampa tutti gli studenti nel registro"""
        conn = DBconnection.db_connection(dbName)
        cursor = conn.cursor()
        
        conn.commit()
        query = "SELECT * FROM studenti"
        cursor.execute(query)
        result = cursor.fetchall()
        
        for row in result:
            print(row)
            
        conn.close()


def main():
    """Funzione principale che gestisce il menu"""
    # Crea un'istanza del registro studenti
    register = Register()

    while True:
        try:
            ch = int(input(
                "\n--- Menu ---\n"
                " 1) Visualizza studenti\n"
                " 2) Aggiungi studenti\n"
                " 3) Aggiungi 1 voto per materia a uno studente\n"
                " 4) Aggiungi voto per specifica materia\n"
                " 5) Miglior studente\n"
                " 6) Elimina studente\n"
                " 7) Esci\n"
                " ---> "
            ))
        except ValueError:
            print("Inserisci un numero valido.")
            continue

        match ch:
            case 1:
                register.print_all_student()
            case 2:
                register.add_student()
            case 3:
                stud_id = int(input("Inserisci l'ID dello studente: "))
                if stud_id in register.student:
                    register.student[stud_id].add_all_valutation()
                else:
                    print("Studente non trovato.")
            case 4:
                stud_id = int(input("Inserisci l'ID dello studente: "))
                if stud_id in register.student:
                    register.student[stud_id].add_one_valutation()
                else:
                    print("Studente non trovato.")
            case 5:
                register.best_student()
            case 6:
                register.delete_student()
            case 7:
                print("Uscita dal programma...")
                break
            case _:
                print("Scelta non valida.")

        # Chiede all'utente se vuole tornare al menu
        if input("Vuoi tornare al menu? (s/n) ---> ").strip().lower() == "n":
            break

# Crea le tabelle e avvia il programma
create()
main()