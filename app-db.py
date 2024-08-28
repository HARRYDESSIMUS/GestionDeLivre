import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Créer la table pour les livres
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            disponible BOOLEAN NOT NULL,
            date_emprunt DATE,
            date_retour DATE
        )
    ''')

    # Créer la table pour les membres
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            identifiant TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()