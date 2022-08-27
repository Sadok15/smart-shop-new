import os

from flask import jsonify, render_template, request, Flask, session, flash
from werkzeug.utils import secure_filename

from ia_python.connexion import getRealId
from . import app
from .models import Products
from .utils import voice_detection, stat_prod, stat_prod_dispo, stat_cat, allowed_file


@app.route('/detect_product_voice', methods=['POST'])
def detect_product_voice():
    result = voice_detection()
    result = result.replace("/", "")
    result = result.replace("'", "")
    voice_str = result.split(" ")
    tmp = []
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    for word in voice_str:
        if len(word) >= 4:
            res = Products().get(word)
            if res:
                tmp.append(res)
    if tmp:
        return render_template('Homepages/index.html', produits=tmp[0], nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(),
                               nb_cat=stat_cat(), etat=etat)
    return render_template('Homepages/index.html', produits=[], nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(),
                           nb_cat=stat_cat(), etat=etat)


@app.route('/detect_product_voice_prod/<id_cat>', methods=['POST'])
def detect_product_voice_prod(id_cat):
    result = voice_detection()
    result = result.replace("/", "")
    result = result.replace("'", "")
    voice_str = result.split(" ")
    tmp = []
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    for word in voice_str:
        if len(word) >= 4:
            res = Products().get(word)
            if res:
                tmp.append(res)
    if tmp:
        return render_template('Homepages/produit.html', produits=tmp[0], id_cat=id_cat, etat=etat)
    return render_template('Homepages/produit.html', produits=[], id_cat=id_cat, etat=etat)


'''@app.route('/get_produits_by_libelle/<libelle>', methods=['GET'])
def get_produits_by_libelle(libelle):
    result = Products.get_produits_by_libelle(libelle)
=======
@app.route('/get_produits_by_cat/<id_cat>', methods=['GET'])
def get_produits_by_cat(id_cat):
    real_id_cat = getRealId("id", "categories", id_cat)
    if real_id_cat is None:
        response = {
            "message": f"Aucun produits  correspant a id_produit : '{id_cat}'"
        }
        return jsonify(response), 406
    result = Products.get_produits_by_categorie(real_id_cat)
>>>>>>> f57e380bcc99c086f7b2cb84f65f314cd9ab0f03
    if result:
        return (
            jsonify(
                {"error": False, "etat_opp_list": [item.__dict__ for item in result]}
            ),
            200,
        )
    return (
        jsonify(
            {"error": True, "etat_opp_list": []}
        ),
        204,
    )
'''


@app.route('/get_produits_by_cat/<id_cat>', methods=['GET'])
def get_produits_by_cat(id_cat):
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    real_id_cat = getRealId("id", "categories", id_cat)
    if real_id_cat is None:
        response = {
            "message": f"Aucun categorie  correspant a id_cat : '{id_cat}'"
        }
        return jsonify(response), 406
    result = Products.get_produits_by_categorie(real_id_cat)
    if result:
        return render_template('Homepages/produit.html', produits=[item.__dict__ for item in result], id_cat=id_cat,
                               etat=etat)


@app.route('/get_list_produits', methods=['GET'])
def get_list_produits():
    session.clear()
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    result = Products.list()
    if result:
        return render_template('Homepages/index.html', produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat)


@app.route('/filtre_produit', methods=['POST'])
def filtre_produit():
    data = {
        "disponible": request.form.get("disponible"),
        "libelle": request.form.get("libelle"),
        "prix_min": request.form.get("prix_min"),
        "prix_max": request.form.get("prix_max"),
    }
    result = Products(**data).filtre()
    if result:
        return render_template('Homepages/index.html', produits=result)
    return render_template('Homepages/index.html', produits=result)


@app.route('/filtre_produit_cat/<id_cat>', methods=['POST'])
def filtre_produit_cat(id_cat):
    data = {
        "disponible": request.form.get("disponible"),
        "libelle": request.form.get("libelle"),
        "prix_min": request.form.get("prix_min"),
        "prix_max": request.form.get("prix_max"),
    }
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    result = Products(**data).filtre()
    if result:
        return render_template('Homepages/produit.html', produits=result, id_cat=id_cat, etat=etat)
    return render_template('Homepages/produit.html', produits=[], id_cat=id_cat, etat=etat)


# -----------------------  Gestion du produit Admin -------------------------

@app.route('/Admin/insert_produit', methods=['POST'])
def insert_produit():
    app = Flask(__name__)
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    filename= ""
    if 'file' not in request.files:
        result = Products.list()
        flash("Saisir un fichier pour ce  produit", "error")
        return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                               session=session)

    file = request.files["file"]
    if file.filename == '':
        flash("No file selected for uploading", "error")

    if file and allowed_file(file.filename):
        UPLOAD_FOLDER = 'C:\\Users\\DELL\\PycharmProjects\\IA\\ia_python\\static\\images_produits'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    data = {
        "image": filename,
        "libelle": request.form.get("libelle"),
        "id_cat": request.form.get("id_cat"),
        "prix": request.form.get("prix"),
        "quantite": request.form.get("quantite"),
    }
    produit = Products(**data)
    insert = produit.insert_produit_admin()
    result = Products.list()
    if insert > 0:
        flash("Produit ajouter avec succés", "success")
        return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                               session=session)
    flash("Oops un erreur se produit lors de l'insertion", "danger")
    return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                           nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                           session=session)


@app.route('/Admin/update_produit/<id_prod>', methods=['POST'])
def update_produit(id_prod):
    data = {
        "id": id_prod,
        "libelle": request.form.get("libelle"),
        "prix": request.form.get("prix"),
        "quantite": request.form.get("quantite"),
    }
    produit = Products(**data)
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    result = Products.list()
    if produit.update_produit_admin() == 0:
        flash("Produit modifier avec succés", "success")
        return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                               session=session)
    flash("Oops un erreur se produit lors de la modification", "danger")
    return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                           nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                           session=session)


@app.route('/Admin/delete_produit/<id_prod>', methods=['POST'])
def delete_produit(id_prod):
    result = Products(id=id_prod).delete_produit()
    if result > 0:
        flash("Produit supprimer", "success")
        return render_template("Admin/dashbord.html")
    flash("Oops un erreur se produit lors de la suppression", "danger")
    return render_template("Admin/dashbord.html")


@app.route('/Admin/get_list_produits_admin', methods=['GET'])
def get_list_produits_admin():
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    result = Products.list()
    if result:
        return render_template("Admin/dashbord.html", produits=[item.__dict__ for item in result],
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(), etat=etat,
                               session=session)


@app.route('/Admin/get_produits_by_cat_admin/<id_cat>', methods=['GET'])
def get_produits_by_cat_admin(id_cat):
    if not session:
        etat = "non connecter"
    else:
        etat = "connecter"
    real_id_cat = getRealId("id", "categories", id_cat)
    if real_id_cat is None:
        response = {
            "message": f"Aucun categorie  correspant a id_cat : '{id_cat}'"
        }
        return jsonify(response), 406
    result = Products.get_produits_by_categorie(real_id_cat)
    if result:
        return render_template('Admin/dashbord.html', produits=[item.__dict__ for item in result], id_cat=id_cat,
                               etat=etat,
                               nb_prod=stat_prod(), nb_dispo=stat_prod_dispo(), nb_cat=stat_cat(),
                               )
