from flask import Flask 
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)
FLAG_SQLI = "VULNLAB{sql_lnj3ctl0n_l0gln}"
connection = sqlite3.connect("database_user.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS example (id, Name, User)")
connection.commit()
cursor.execute("SELECT * FROM example WHERE Name = ?", ("alice",))

resultat = cursor.fetchall()

if not resultat:
    cursor.execute("INSERT INTO example VALUES (1, 'alice', 'Admin')")
    connection.commit()


@app.route("/")
def startLab():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["pass"]

        requete = f"SELECT * FROM example WHERE Name = '{username}' AND User = '{password}'"
        print(requete)

        try:
            cursor.execute(requete)
            resultat = cursor.fetchall()

            if resultat:
                if username == "alice" and password == "Admin":
                    print("Connexion normale")
                else:
                    print("SQL Injection réussie !")
                    print(FLAG_SQLI)
            else:
                print("Identifiants incorrects")

        except sqlite3.Error:
            print("Erreur SQL")

    return render_template("login.html")
app.run()
