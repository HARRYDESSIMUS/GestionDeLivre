from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta, date


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/livres')
def afficher_livres():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('livres.html', livres=livres)

@app.route('/ajouter_livre', methods=('GET', 'POST'))
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        isbn = request.form['isbn']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, isbn, disponible) VALUES (?, ?, ?, ?)',
                     (titre, auteur, isbn, True))
        conn.commit()
        conn.close()
        return redirect(url_for('afficher_livres'))
    return render_template('ajouter_livre.html')

@app.route('/emprunter_livre/<int:id>', methods=('POST',))
def emprunter_livre(id):
    conn = get_db_connection()
    livre = conn.execute('SELECT * FROM livres WHERE id = ?', (id,)).fetchone()
    if livre and livre['disponible']:
        date_emprunt = datetime.now().date()
        date_retour = date_emprunt + timedelta (days=14)  # Par exemple, 14 jours pour le retour
        conn.execute('''
            UPDATE livres
            SET disponible = ?, date_emprunt = ?, date_retour = ?
            WHERE id = ?
        ''', (False, date_emprunt, date_retour, id))
        conn.commit()
    conn.close()
    return redirect(url_for('afficher_livres'))

@app.route('/retourner_livre/<int:id>', methods=('POST',))
def retourner_livre(id):
    conn = get_db_connection()
    livre = conn.execute('SELECT * FROM livres WHERE id = ?', (id,)).fetchone()
    if livre and not livre['disponible']:
        conn.execute('''
            UPDATE livres
            SET disponible = ?, date_emprunt = ?, date_retour = ?
            WHERE id = ?
        ''', (True, None, None, id))
        conn.commit()
    conn.close()
    return redirect(url_for('afficher_livres'))