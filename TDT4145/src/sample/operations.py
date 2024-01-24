import sqlite3
import shared

# Denne funksjonen brukes for å sette inn flere data-poster i databasen. Den tar inn to parametere: query, som er SQL-spørringen for å sette inn data, og data, som er en liste over dataposter som skal settes inn. Funksjonen åpner en forbindelse til databasen, oppretter en cursor og utfører deretter spørringen ved hjelp av executemany()-metoden. Til slutt blir forbindelsen lukket.#


def insert_data(query, data):
    conn = sqlite3.connect(shared.db_name)
    cursor = conn.cursor()

    try:
        cursor.executemany(query, data)
    except AttributeError:
        pass
    conn.commit()
    conn.close()

# Denne funksjonen utfører en SQL-spørring som returnerer data fra databasen. Den tar inn query, som er SQL-spørringen, og params, som er en tuple med parameterverdier som skal brukes i spørringen (hvis noen). Funksjonen åpner en forbindelse til databasen, oppretter en cursor og utfører deretter spørringen. Resultatet av spørringen blir hentet ved hjelp av fetchall()-metoden, og forbindelsen lukkes før funksjonen returnerer resultatet.


def read(query, params=None):
    conn = sqlite3.connect(shared.db_name)
    c = conn.cursor()

    if params:
        c.execute(query, params)
    else:
        c.execute(query)
    column_names = [description[0] for description in c.description]
    rows = c.fetchall()
    rows.insert(0, column_names)
    conn.close()

    return rows

# Denne funksjonen brukes til å utføre SQL-spørringer som endrer databasen. Den tar inn query, som er SQL-spørringen, og params, som er en tuple med parameterverdier som skal brukes i spørringen (hvis noen). Funksjonen åpner en forbindelse til databasen, oppretter en cursor og utfører deretter spørringen. Til slutt blir endringene lagret ved hjelp av commit()-metoden, og forbindelsen lukkes.


def write(query, params=None):
    conn = sqlite3.connect(shared.db_name)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()
