import traceback

import requests
from flask import jsonify, render_template, request, session, flash

from products.models import Products
from products.utils import stat_prod, stat_cat, stat_prod_dispo
from . import app
from .model import Authentifiaction
from .utils import add_face_auth, check_face_auth

# ------------------------ path --------------------------------



@app.route('/se_connecter', methods=['GET'])
def se_connecter():
    session.clear()
    return render_template('login/se_connecter.html')


@app.route('/inscription_page', methods=['POST'])
def inscription_page():
    return render_template('login/inscription.html')


@app.route('/inisialisation_mdp/<mail>', methods=['GET'])
def inisialisation_mdp(mail):
    session['mail'] = mail
    return render_template('login/nouveau_mdp.html')


@app.route('/deconnexion', methods=['GET'])
def deconnexion():
    return render_template('login/se_connecter.html')


@app.route('/acceuil', methods=['GET'])
def acceuil():
    return render_template('Homepages/index.html')


@app.route('/profile', methods=['GET'])
def profile():
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    return render_template('Homepages/profile.html', session=session, etat=etat)


# ----------------------------- WS ------------------------------

@app.route('/check_auth', methods=['POST'])
def check_auth():
    session.clear()
    mail = request.form.get("mail")
    password = request.form.get("password")
    if mail and password:
        auth = Authentifiaction(mail=mail, password=password)
        user = auth.get()
        if user:
            session['mail'] = user['mail']
            session['password'] = user['password']
            session['image'] = user['image']
            session['name'] = user['name']
            session['lastname'] = user['lastname']
            session['id'] = user['id']
            etat = "connecter"
            result = Products.list()
            if user['identite'] == "C":
                if result:
                    return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                                           nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(),
                                           etat=etat,
                                           session=session)
            elif user['identite'] == "A":
                print([item.__dict__ for item in result])
                return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                                       nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                                       session=session)

        flash("Erreur: Vérifier vos données", "danger")
        return render_template('login/se_connecter.html')


@app.route('/inscription', methods=['POST'])
def inscription():
    mail = request.form.get("mail")
    password = request.form.get("password")
    name = request.form.get("name")
    lastname = request.form.get("lastname")

    result = add_face_auth(mail, password, name, lastname)

    if result > 0:
        session['mail'] = mail
        session['password'] = password
        session['name'] = name
        session['lastname'] = lastname
        session['id'] = result
        etat = "connecter"
        result = Products.list()
        return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                               session=session)
    elif result == -1:
        flash("Vous avez deja un compte", "danger")
        return render_template('login/se_connecter.html')

    else:
        flash("Oops Un erreur se produit", "danger")
        render_template('login/inscription.html')


@app.route("/mdp_oublier", methods=["POST"])
def mdp_oublier():
    mail = request.form.get("mail")
    if mail:
        session['mail'] = mail
        result = Authentifiaction(mail=mail).verify()
        if result == "SENDED":
            flash("Vérifier votre boite mail svp", "success")
            return render_template('login/se_connecter.html')
        elif result == "ERROR":
            flash("Adresse mail invalide", "danger")
            return render_template('login/se_connecter.html')

        flash("Oops un probleme se deroule lors de l'execution", "danger")
        return render_template('login/se_connecter.html')


@app.route("/sauvgarde_nv_mdp", methods=["GET"])
def sauvgarde_nv_mdp():
    mdp = request.args.get("mdp")
    cmdp = request.args.get("cmdp")

    if mdp and cmdp:
        if cmdp != mdp:
            flash("La confirmation du mot de passe est incorrecte", "danger")
            return render_template('login/nouveau_mdp.html')
        auth = Authentifiaction(mail=session['mail'], password=mdp)
        result = auth.update_password()
        if result == "MODIFIED":
            session['password'] = mdp
            flash("Modification avec succes , saisir votre coordonnées", "success")
            return render_template('login/se_connecter.html')

        flash("Erreur lors de la modification", "danger")
        return render_template('login/nouveau_mdp.html')
    flash("Saisir votre mot de passe", "danger")
    return render_template('login/nouveau_mdp.html')


@app.route('/connexion_visage', methods=['POST'])
def connexion_visage():
    try:
        # mail = request.form.get("mail")
        # session['mail'] = mail
        result = check_face_auth()
        if result:
            etat = "connecter"
            result = Products.list()
            if result:
                return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                                       nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                                       session=session)
        flash("Oops un erreur se produit", "danger")
        return render_template('login/se_connecter.html')
    except:
        print(traceback.format_exc())
        flash("Oops un erreur se produit", "danger")
        return render_template('login/se_connecter.html')


@app.route('/update_user', methods=['POST'])
def update_user():
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    mail = session['mail']
    if name and lastname:
        auth = Authentifiaction(name=name, lastname=lastname, mail=mail)
        result = auth.update_user()
        if result == 0:
            session['name'] = name
            session['lastname'] = lastname
            flash('Modification avec succés', "success")
            return render_template("Homepages/profile.html", session=session, etat=etat)
        flash('Erreur lors de la modification', "danger")
        return render_template("Homepages/profile.html", session=session, etat=etat)
    flash('Aucune modification', "danger")
    return render_template("Homepages/profile.html", session=session, etat=etat)
