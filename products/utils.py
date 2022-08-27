import speech_recognition as sr
from flask import Flask, jsonify

from connexion import selectqueryfetchone
from googletrans import Translator
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def voice_detection():
    trans = Translator()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak : ')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text:
                result = trans.translate(text, dest='fr')
                return result.text

        except:
            print("Sorry Try Again")
            return "ERROR"


def stat_prod():
    query = "SELECT COUNT(*) FROM products"
    return selectqueryfetchone(query)


def stat_prod_dispo():
    prod = stat_prod()
    query = "SELECT COUNT(*) FROM products WHERE quantite > 0"
    dispo = selectqueryfetchone(query)
    if prod and dispo:
        return 100 * dispo / prod
    return 0

def stat_cat():
    query = "SELECT COUNT(*) FROM categories"
    return selectqueryfetchone(query)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS