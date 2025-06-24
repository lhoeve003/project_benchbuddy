# Voor onderstaande delen van de code is AI geraadpleegd,
# in combinatie met benoemde bronnen.
# De SQL-query's (c.execute) voor de functies init_db en save_data.


# Importeer de sqlite3 module voor het werken met SQlite database.
import sqlite3

# Zorgt voor verbinding met SQLite database en het maken van de tabel.


def init_db():
    # Maakt een verbinding met een SQLite database bestandje.
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
    # Check_same_thread=False voorkomt foutmeldingen,
    # Wanneer je vanuit verschillende delen van je applicatie bij de database probeert te komen.
    conn = sqlite3.connect('benchbuddy_data.db', check_same_thread=False)

    # Maakt een object voor de cursor om SQL statements mee uit te voeren:
    # Verwerkt rijen uit resultaat set één voor één, in plaats van alle rijen tegelijk.
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.cursor
    c = conn.cursor()

    # Vertelt de database wat gedaan moet worden.
    # Voert SQL query uit zoals SELECT, INSERT, DELETE, etc.
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
    c.execute('''
        CREATE TABLE IF NOT EXISTS experiment_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            input TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Bovenstaande wordt gemaakt voor het opslaan van experiment gegevens:
    # Database wordt gemaakt als deze nog niet bestaat.
    # ID: maakt een kolom id aan met een uniek nummer voor elke rij.
    # Drie tekstkolommen aan: type, input en result.
    # Timestamp: maakt een kolom waarbij automatisch tijd en datum wordt toegevoegd.
    # https://www.w3resource.com/PostgreSQL/snippets/postgresql-create-table-if-not-exists.php

    # Alle veranderingen met SQL worden hiermee opgeslagen in de database.
    conn.commit()

    # Geeft de verbinding en cursor terug voor verder gebruik.
    return conn, c


# Deze functie stopt gegevens in database en zorgt dat ze opgeslagen blijven
def save_data(c, conn, type_, input_, result):
    # Voeg nieuwe rij toe aan de tabel:
    # Type, input en result krijgen de waarde die zijn ingevoerd.
    # Het vraagteken zijn plaatsvervangers voor echte waarden die je kan invullen:
    # Voorkomt SQL injectie: https://www.sqlitetutorial.net/sqlite-python/insert/
    c.execute("INSERT INTO experiment_data (type, input, result) VALUES (?, ?, ?)",
              (type_, input_, result))

    # Slaat de wijzigingen op in de database
    conn.commit()
