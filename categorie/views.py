from flask import jsonify
from . import app
from categorie.models import Categories
from connexion import getRealId


@app.route('/get_categories_by_id/<id_cat>', methods=['GET'])
def get_produits_by_id(id_cat):
    real_id = getRealId("id", "categories", id_cat)
    if real_id is None:
        response = {
            "message": f"Aucune categories  correspant a id_produit : '{id_cat}'"
        }
        return jsonify(response), 406
    result = Categories.get(real_id)
    if result:
        return (
            jsonify(
                {"error": False, "cat": result.__dict__}
            ),
            200,
        )
    return (
        jsonify(
            {"error": True, "cat": None}
        ),
        204,
    )

@app.route('/get_categories_by_libelle/<libelle>', methods=['GET'])
def get_produits_by_libelle(libelle):
    result = Categories.get_categorie_by_libelle(libelle)
    if result:
        return (
            jsonify(
                {"error": False, "cat_list": [item.__dict__ for item in result]}
            ),
            200,
        )
    return (
        jsonify(
            {"error": True, "cat_list": []}
        ),
        204,
    )


@app.route('/get_list_categories', methods=['GET'])
def get_list_produits():
    result = Categories.list()
    if result:
        return (
            jsonify(
                {"error": False, "cat_list": [item.__dict__ for item in result]}
            ),
            200,
        )
    return (
        jsonify(
            {"error": True, "cat_list": []}
        ),
        204,
    )