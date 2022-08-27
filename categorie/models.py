from connexion import modelselectquery, model_select_query_fetch_one, insertquery


class Categories():
    def __init__(
            self,
            id=None,
            libelle=None,

            **kwargs,
    ):
        self.id = id
        self.libelle = libelle

    @classmethod
    def get_categorie_by_libelle(cls,libelle):
        query=f"SELECT * FROM categories WHERE libelle  like '%{libelle}%'"
        result = modelselectquery(query,cls)
        if result :
            return result
        return None

    @classmethod
    def get(cls, id):
        query = f"SELECT * FROM categories WHERE id ='{id}'"
        return model_select_query_fetch_one(query, cls) or []
    @classmethod
    def get_produits_by_categorie(cls,id_cat):
        query=(f"SELECT * FROM products WHERE produits.id_cat = '{id_cat}'")
        return modelselectquery(query,cls) or []

    @classmethod
    def list(cls):
        query=f"SELECT * FROM categories"
        print(query)
        return  modelselectquery(query,cls) or []


    def insert(self):
        query=f"INSERT INTO categories SET libelle = '{self.libelle}'  "
        if insertquery(query) > 0 :
            return "ROW ADDED"
        return "ERROR"

