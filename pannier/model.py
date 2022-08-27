from connexion import insertquery, deletequery, modelselectquery, select_query_fetch_one, updatequery, \
    selectqueryfetchone
from products.models import Products


class Pannier():
    def __init__(
            self,
            id_user=None,
            id_prod=None,
            quantite=None,

            **kwargs,
    ):
        self.id_user = id_user
        self.id_prod=id_prod
        self.quantite=quantite


    def add_pannier(self):
        self.quantite=self.get_quantite_prod()
        if self.quantite :
            return self.max_quantite()
        return self.insert_prod()

    def insert_prod(self):
        query = f"insert into panier set id_user='{self.id_user}' , id_prod='{self.id_prod}' , quantite=1 "
        return insertquery(query)

    def min_quantite(self):
        self.quantite=self.get_quantite_prod()
        if self.quantite :
            if self.get_quantite_prod() > 0:
                self.quantite -= 1
                return self.update_quantite()
            self.delete_pannier()
            return 0
        return 1


    def update_quantite(self):
        query = f"Update panier set quantite='{self.quantite}' where id_prod='{self.id_prod}' and id_user ='{self.id_user}' "
        return updatequery(query)

    def max_quantite(self):
        self.quantite = self.get_quantite_prod()
        if self.quantite :
            self.quantite += 1
            return self.update_quantite()

    def delete_pannier(self):
        query=f"Delete from panier where id_prod = '{self.id_prod}' and id_user='{self.id_user}' "
        return deletequery(query)


    def get_quantite_prod(self):
        query = f"select quantite from panier where id_prod='{self.id_prod}' and id_user ='{self.id_user}'"
        return selectqueryfetchone(query)

    @classmethod
    def get(cls,id_user):
        response=[]
        query=f"select * from panier where id_user='{id_user}' "
        result=modelselectquery(query, cls)
        for res in result :
            product=Products.get_by_id(res.id_prod)
            product.quantite_pannier=res.quantite
            product.total_prod=product.quantite_pannier*product.prix
            response.append(product.__dict__)
        return response
    @classmethod
    def get_total_pannier(cls,id_user):
        total=0
        list_prod=Pannier.get(id_user)
        for prod in list_prod :
            total+=prod['total_prod']
        return total

    def vider_pannier(self):
        query=f"Delete from panier where id_user='{self.id_user}' "
        return deletequery(query)