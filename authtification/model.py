
from flask import Flask
from flask_mail import Mail, Message

from connexion import updatequery, select_query_fetch_one, insertquery, selectqueryfetchone

app = Flask(__name__)

setting = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "sadokfrouja1im8@gmail.com",
    "MAIL_PASSWORD": "SADOK.98"
}

app.config.update(setting)

class Authentifiaction :
    def __init__(
            self,
            id=None,
            mail=None,
            password=None,
            name=None,
            lastname=None,
            image=None,
            **kwargs
    ):
        self.id = id
        self.mail = mail
        self.password = password
        self.name = name
        self.lastname = lastname
        self.image = image

    def insert(self):
        result = select_query_fetch_one(f"SELECT * FROM auth WHERE mail = '{self.mail}'")
        if not result :
            return insertquery(f"INSERT INTO auth SET mail = '{self.mail}' , password = '{self.password}' ,"
                                  f" name = '{self.name}', lastname = '{self.lastname}' , image = '{self.image}' ")
        return -1

    def get(self):
        query= f"SELECT * FROM auth WHERE mail = '{self.mail}' and password = '{self.password}'"
        return select_query_fetch_one(query)

    def update_user(self):
        query= f"UPDATE auth SET name='{self.name}' , lastname='{self.lastname}' WHERE mail='{self.mail}' "
        return updatequery(query)

    def get_param_by_image(self):
        return select_query_fetch_one(f"SELECT * FROM auth WHERE image = '{self.image}'")

    def verify(self):
        query = f"SELECT * FROM auth WHERE mail = '{self.mail}' "
        result = select_query_fetch_one(query)
        if result:
            mail = Mail(app)
            recipient = self.mail
            with app.app_context():
                msg = Message(subject="Réinisilisation Mot De Passe", sender="sadokfrouja1im8@gmail.com",
                              recipients=[recipient])
                msg.body = f"Saisir Votre nouveau mot de passe ici : http://127.0.0.1:5000/inisialisation_mdp/{recipient}"
                mail.send(msg)
            return "SENDED"
        return "ERROR"

    def update_password(self):
        result = updatequery(f"UPDATE  auth SET password = '{self.password}'  WHERE mail='{self.mail}' ")
        if result == 0:
            return "MODIFIED"
        return "ERROR"

    def get_user_image(self):
        result = selectqueryfetchone(f"SELECT image FROM auth WHERE mail = '{self.mail}' ")
        if result:
            return result