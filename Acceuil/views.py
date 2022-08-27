from flask import render_template
from . import app


@app.route('/Acceuil', methods=['GET'])
def Acceuil():
    return render_template('Homepages/index.html')
