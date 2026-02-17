import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS giochi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero_giocatori_massimo INTEGER NOT NULL,
            durata_media INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return redirect(url_for("nuovo_gioco"))


@app.route("/giochi/nuovo", methods=["GET", "POST"])
def nuovo_gioco():
    errore = ""

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_giocatori_massimo_raw = request.form.get("numero_giocatori_massimo", "")
        durata_media_raw = request.form.get("durata_media", "")
        categoria = request.form.get("categoria", "").strip()

        try:
            numero_giocatori_massimo = int(numero_giocatori_massimo_raw)
            durata_media = int(durata_media_raw)
        except ValueError:
            errore = "Numero giocatori e durata devono essere numeri interi."

        if not errore:
            if not nome or not categoria:
                errore = "Compila tutti i campi."
            elif numero_giocatori_massimo <= 0 or durata_media <= 0:
                errore = "Numero giocatori e durata devono essere maggiori di 0."

        if not errore:
            conn = sqlite3.connect("database.db")
            conn.execute(
                """
                INSERT INTO giochi (nome, numero_giocatori_massimo, durata_media, categoria)
                VALUES (?, ?, ?, ?)
                """,
                (nome, numero_giocatori_massimo, durata_media, categoria),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("nuovo_gioco", creato=1))

    creato = request.args.get("creato") == "1"
    return render_template("nuovo_gioco.html", errore=errore, creato=creato)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
