from connexion import modelselectquery, selectquery, model_select_query_fetch_one

from ia_python.connexion import insertquery, updatequery


class Products():
    def __init__(
            self,
            id=None,
            libelle=None,
            image=None,
            id_cat=None,
            categorie=None,
            prix=None,
            quantite=None,
            disponible=None,
            prix_min=None,
            prix_max=None,
            quantite_pannier=None,
            total_prod=None,
            **kwargs,
    ):
        self.total_prod=total_prod
        self.quantite_pannier=quantite_pannier
        self.id = id
        self.libelle = libelle
        self.image = image
        self.id_cat = id_cat
        self.categorie = categorie
        self.prix = prix
        self.quantite = quantite
        self.disponible = disponible
        self.prix_min = prix_min
        self.prix_max = prix_max

    @classmethod
    def get_produits_by_libelle(cls, libelle):
        query = f"SELECT * FROM products WHERE libelle  like '%{libelle}%'"
        result = modelselectquery(query, cls)
        if result:
            return result
        return None

    def get(self, word):
        query = f"SELECT * FROM products WHERE LOWER(libelle) Like '%{word.lower()}%'"
        return selectquery(query) or []
    @classmethod
    def get_by_id(cls, id_prod):
        query = f"SELECT * FROM products WHERE id = '{id_prod}'"
        return model_select_query_fetch_one(query,cls) or []

    @classmethod
    def get_produits_by_categorie(cls, id_cat):
        query = (f"SELECT * FROM products WHERE products.id_cat = '{id_cat}'")
        return modelselectquery(query, cls) or []

    @classmethod
    def list(cls):
        query = f"SELECT p.*,c.libelle as 'categorie' FROM products p LEFT JOIN categories c on p.id_cat = c.id"
        return modelselectquery(query, cls) or []

    def insert(self):
        query = f"INSERT INTO products SET libelle = '{self.libelle}' , image = '{self.image}' , id_cat='{self.id_cat}' "
        if insertquery(query) > 0:
            return "ROW ADDED"
        return "ERROR"

    def filtre(self):
        query = "SELECT * FROM products WHERE "
        nb = 0
        if self.libelle:
            nb += 1
            query += f" AND libelle like '%{self.libelle}%' "
        if self.disponible:
            if self.disponible.lower() == "oui":
                nb += 1
                query += " AND quantite > 0 "
            elif self.disponible.lower() == "non":
                nb += 1
                query += " AND quantite = 0 "
        if self.prix_min:
            nb += 1
            query += f" AND prix > '{self.prix_min}' "
        if self.prix_max:
            nb += 1
            query += f" AND prix < '{self.prix_max}' "
        if nb > 0:
            if nb == 1:
                query = query[0:30] + query[33:]
            return selectquery(query)
        return []

    def update_produit_admin(self):
        return updatequery(f"UPDATE products SET libelle='{self.libelle}' , prix='{self.prix}' , quantite='{self.quantite}' WHERE id = '{self.id}' ")

    def insert_produit_admin(self):
        return insertquery(f"INSERT INTO products SET libelle='{self.libelle}' ,"
                           f" image='{self.image}' , prix='{self.prix}' , quantite='{self.quantite}' , id_cat='{self.id_cat}'")