from flask import Flask
from flask_cors import CORS
import webbrowser
from authtification import app as auth_app
from products import app as prod_app
from Acceuil import app as acceuil_app
from categorie import  app as cat_app
from pannier import  app as pannier_app
app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

app.register_blueprint(auth_app)
app.register_blueprint(prod_app)
app.register_blueprint(acceuil_app)
app.register_blueprint(cat_app)
app.register_blueprint(pannier_app)

if __name__ == "__main__" :
    app.config["DEBUG"] = True
    webbrowser.open('http://localhost:5000/get_list_produits')
    app.run()