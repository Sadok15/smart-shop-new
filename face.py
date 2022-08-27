import os
import shutil
from datetime import datetime
import cv2
import face_recognition


'''def time_is_up():
    # Faire quelque chose une fois le temps écoulé.
    widget['text'] = "Time is UP !"


def wait(remaining_time, callback):
    remaining_time -= 1
    widget['text'] = "Temps restant : {}".format(remaining_time)
    if remaining_time > 0:
        widget.after(1000, wait, remaining_time, callback)
    else:
        callback()'''

'''# ------------- tkinter root ---------------
root = Tk()
# Et au moment où on veut lancer le timer:
widget = Label(root, text="Temps restant : 5")
widget.pack()
widget.after(1000, wait, 20, time_is_up)

root.mainloop()'''


face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


ret,img = cap.read()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.1,4)
for (x,y,w,h) in faces :
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)

cv2.imshow('img',img)
k = cv2.waitKey(30) & 0xff

image_name = str(datetime.now().strftime("%H:%M:%S")).replace(":","_") + ".jpg"
cv2.imwrite(image_name, img)

cap.release()
cv2.destroyAllWindows()

shutil.move(f"{image_name}","unknown_images")


#----------- compare faces ---------------

list_knonw_img = os.listdir("known_images")

if len(list_knonw_img) :
    for image in list_knonw_img :
        known_image = face_recognition.load_image_file(f"known_images/{image}")
        unknown_image = face_recognition.load_image_file(f"unknown_images/{image_name}")

        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        print(results)

    os.remove(f"unknown_images/{image_name}")

