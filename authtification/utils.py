import os
import shutil
from datetime import datetime
import cv2
import face_recognition

from authtification.model import Authentifiaction
from flask import session


def add_face_auth(mail,password,name,lastname):

    face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff

    image_name = mail + '_' +str(datetime.now().strftime("%H:%M:%S")).replace(":", "_") + ".jpg"
    cv2.imwrite(image_name, img)

    #---------- add image to specific user ----------
    auth = Authentifiaction(mail=mail, password=password, name=name, lastname=lastname,image=str(image_name))
    result = auth.insert()
    if result == "ROW ADDED":
        session['image'] = str(image_name)
        shutil.move(f"{image_name}", "known_images")
    else  :
        os.remove(f"{image_name}")
    cap.release()
    cv2.destroyAllWindows()

    return result

def check_face_auth():

    face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff

    image_name = str(datetime.now().strftime("%H:%M:%S")).replace(":", "_") + ".jpg"
    cv2.imwrite(image_name, img)

    cap.release()
    cv2.destroyAllWindows()

    shutil.move(f"{image_name}", "unknown_images")

    # ----------- compare faces ---------------

    list_knonw_img = os.listdir("known_images")

    if len(list_knonw_img):
        data_len = len(list_knonw_img)
        i = 0
        #auth = Authentifiaction(mail=mail)
        #db_image = auth.get_user_image()
        #auth.image= db_image

        #if db_image :
        for image in list_knonw_img:
            #if image == db_image:
            known_image = face_recognition.load_image_file(f"known_images/{image}")
            unknown_image = face_recognition.load_image_file(f"unknown_images/{image_name}")

            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            i += 1
            if results[0] == True :
                auth = Authentifiaction(image=image)
                data = auth.get_param_by_image()
                if data :
                    session['mail'] = data['mail']
                    session['password'] = data['password']
                    session['image'] = data['image']
                    session['name'] = data['name']
                    session['lastname'] = data['lastname']
                    session['id'] = data['id']
                    os.remove(f"unknown_images/{image_name}")
                    return data
            elif i >= data_len :
                similar_image = None
                os.remove(f"unknown_images/{image_name}")
                return similar_image
        #return "ERROR"


