from datetime import datetime

from flask import jsonify, flash, render_template, session, make_response
import pdfkit

from . import app

from connexion import getRealId
from .model import Pannier
from products.models import Products
from products.utils import stat_prod, stat_prod_dispo, stat_cat


@app.route('/get_pannier_by_id_user/<id_user>', methods=['GET'])
def get_pannier_by_id_user(id_user):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier.get(real_id)
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result:
        return render_template("Homepages/pannier.html",produits=result,etat=etat,session=session)
    return render_template("Homepages/pannier.html", produits=result, etat=etat,session=session)

@app.route('/insert_produit_into_pannier/<id_user>/<id_prod>', methods=['POST'])
def insert_produit_into_pannier(id_user,id_prod):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun user  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    real_id_prod = getRealId("id", "products", id_prod)
    if real_id_prod is None:
        response = {
            "message": f"Aucun produits  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id,id_prod=real_id_prod).add_pannier()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result == 0 :
        flash('Produit ajouté au panier', "success")
        result = Products.list()
        if result:
            return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                                   nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat)

    flash('erreur s"est produite', "danger")
    return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                           nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat)


@app.route('/insert_produit_into_pannier_cat/<id_user>/<id_prod>/<id_cat>', methods=['POST'])
def insert_produit_into_pannier_cat(id_user,id_prod,id_cat):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun user  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    real_id_prod = getRealId("id", "products", id_prod)
    if real_id_prod is None:
        response = {
            "message": f"Aucun produits  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id,id_prod=real_id_prod).add_pannier()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result == 0 :
        flash('Produit ajouté au panier', "success")
        result = Products.get_produits_by_categorie(id_cat)
        if result:

            return render_template('Homepages/produit.html', produits=[item.__dict__ for item in result],etat=etat,id_cat=id_cat)
    flash('erreur s"est produite', "danger")
    return render_template('Homepages/produit.html', produits=[item.__dict__ for item in result], etat=etat,id_cat=id_cat)


#non encore utilisé
@app.route('/vider_pannier_by_id_user/<id_user>', methods=['DELETE'])
def vider_pannier_by_id_user(id_user):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id).vider_pannier()
    if result > 0 :
        return (
            jsonify(
                {"error": False, "message": 'pannier_vider_avec_succées' }
            ),
            200,
        )
    return (
        jsonify(
            {"error": True,  "message": 'erreur s"est produite' }
        ),
        204,
    )


@app.route('/delete_produit_from_pannier/<id_user>/<id_prod>', methods=['GET'])
def delete_produit_from_pannier(id_user,id_prod):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    real_id_prod = getRealId("id", "products", id_prod)
    if real_id_prod is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id,id_prod=real_id_prod).delete_pannier()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result > 0 :
        flash('Produit retirer du panier', "success")
        result = Pannier.get(real_id)
        if result:
            return render_template("Homepages/pannier.html", produits=result, etat=etat)
    flash('erreur s"est produite', "danger")
    return render_template("Homepages/pannier.html", produits=result, etat=etat)

@app.route('/min_produit_from_pannier/<id_user>/<id_prod>', methods=['GET'])
def min_produit_from_pannier(id_user,id_prod):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    real_id_prod = getRealId("id", "products", id_prod)
    if real_id_prod is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id,id_prod=real_id_prod).min_quantite()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result == 0 :
        flash('Quantité minimiser pour ce produit', "success")
        result = Pannier.get(real_id)
        if result:
            return render_template("Homepages/pannier.html", produits=result, etat=etat)
    flash('erreur s"est produite', "danger")
    return render_template("Homepages/pannier.html", produits=result, etat=etat)

@app.route('/max_produit_from_pannier/<id_user>/<id_prod>', methods=['GET'])
def max_produit_from_pannier(id_user,id_prod):
    real_id = getRealId("id", "auth", id_user)
    if real_id is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    real_id_prod = getRealId("id", "products", id_prod)
    if real_id_prod is None:
        response = {
            "message": f"Aucun contrat  correspant a id_produit : '{id_user}'"
        }
        return jsonify(response), 406
    result = Pannier(id_user=real_id,id_prod=real_id_prod).max_quantite()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    if result == 0 :
        flash('Quantité maximiser pour ce produit', "success")
        result = Pannier.get(real_id)
        if result:
            return render_template("Homepages/pannier.html", produits=result, etat=etat)
    flash('erreur s"est produite', "danger")
    return render_template("Homepages/pannier.html", produits=result, etat=etat)


@app.route('/facture_pdf/<id_user>', methods=['POST'])
def facture_pdf(id_user):
    #pdf = pdfkit.from_string('https://www.google.com/', 'sample.pdf')
    produit=Pannier.get(id_user)
    #path_wkthmltopdf = '/home/dell/.cache/pip/wheels/1b/47/0c/7a2def248029e992e2e8f2fc6bd479cb8648fc6cef2c374deb/wkhtmltopdf-0.2-py3-none-any.whl'

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    wkhtmltopdf_options = {
        'enable-local-file-access': None
    }
    html = render_template(
        "facture_template/index.html",
        mail= session['mail'], name= session['name']+session['lastname'],
        date=datetime.now().strftime("%Y-%m-%d "),produits=produit ,totale=Pannier.get_total_pannier(id_user))
    pdf = pdfkit.from_string(html,False,configuration=config,options=wkhtmltopdf_options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response