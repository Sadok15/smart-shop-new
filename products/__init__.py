from flask import Blueprint

app = Blueprint("Products API", __name__)

import products.views