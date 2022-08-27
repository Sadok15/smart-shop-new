from flask import Blueprint

app = Blueprint("Pannier API", __name__)

import pannier.views