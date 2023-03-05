import json

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
import sqlite3
import uuid

app = Flask(__name__)




@app.route('/')
def acceuil():  # put application's code here
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute('''create table if not exists article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication text,
  paragraphe varchar(500)
);''')
    connection.commit()
    cursor.execute("SELECT * FROM article")
    return render_template('accueil.html')

@app.route('/article/<string:articleid>')
def article(articleid):
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM article WHERE identifiant = "'+articleid+'"')
    if len(cursor.fetchall()) ==0:
        return render_template('error404.html')
    return render_template('article.html')

@app.route('/getarticle/<string:articleid>')
def getarticle(articleid):
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute("SELECT titre,auteur,paragraphe FROM article WHERE identifiant = {} ".format('"'+articleid+'"'))
    res = cursor.fetchall()
    return jsonify({"titre":res[0][0],"auteur":res[0][1],"paragraphe":res[0][2]})

@app.route('/api/acceuil')
def test():
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute("SELECT titre,identifiant,date_publication FROM article ORDER BY date_publication DESC LIMIT 5")
    resultat = [{"titre":i[0],"id":i[1],"date":i[2]}for i in cursor.fetchall()]
    return jsonify(resultat)

@app.route('/api/acceuil/recherche')
def recherche():
    ch = request.args.get("cherche")
    print(ch)
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute("SELECT titre,identifiant,date_publication FROM article WHERE titre LIKE {} OR paragraphe LIKE {}  ORDER BY date_publication DESC LIMIT 5".format('"%'+str(ch)+'%"','"%'+str(ch)+'%"'))
    resultat = [{"titre": i[0], "id": i[1], "date": i[2]} for i in cursor.fetchall()]
    return jsonify(resultat)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admingetall')
def admingetall():
    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute("SELECT titre, identifiant ,date_publication FROM article")
    resultat = [{"titre": i[0], "id": i[1], "date": i[2]} for i in cursor.fetchall()]
    return jsonify(resultat)

@app.route('/modif/<string:articleid>')
def modif(articleid):
    return render_template('modifierarticle.html')

@app.route('/ecraser', methods=['PUT'])
def ecraser():
    titre = request.args.get("titre")
    identifiant = request.args.get("identifiant")
    paragraphe = request.args.get("paragraphe")
    connection = sqlite3.connect('database')
    print(paragraphe,titre,identifiant)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE article SET titre = "' + titre + '", paragraphe = "' + paragraphe + '" WHERE identifiant = "' + identifiant + '"')
    connection.commit()
    return jsonify("ok")

@app.route('/admin-nouveau')
def admin_nouveau():
    return render_template('admin-nouveau.html')

@app.route('/envoyer', methods=['POST'])
def donnees_formulaire():
    titre = request.form['titre']
    print(titre)
    auteur = request.form['auteur']
    print(auteur)
    date_publication = request.form['date_publication']
    print(date_publication)
    paragraphe = request.form['paragraphe']
    print(paragraphe)

    connection = sqlite3.connect('database')
    cursor = connection.cursor()
    cursor.execute('SELECT max(id) FROM article')
    id = cursor.fetchall()[0][0] + 1
    print(titre,auteur,date_publication,paragraphe,id)
    cursor.execute(
        '''INSERT INTO article (id, titre, identifiant, auteur, date_publication, paragraphe) VALUES ({},{},{},{},{},{})'''.format(
            id, '"'+titre+'"', '"'+str(id)+'"', '"'+auteur+'"', '"'+date_publication+'"', '"'+paragraphe+'"'))
    connection.commit()

    return redirect('http://127.0.0.1:5000/admin-nouveau')


if __name__ == '__main__':
    app.run()
