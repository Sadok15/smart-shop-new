import cv2
import numpy as np

#-------------- Load Yolo--------------

net = cv2.dnn.readNet("config/yolov3.weights","config/yolov3.cfg")
classes = []
with open("coco.names","r") as f :
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0,255,size=(len(classes),3))

#------------------ Loading Image -----------------

img = cv2.imread("room_ser.jpg")
img = cv2.resize(img,None,fx=0.5,fy=0.5)
print(img.shape)
height , width , channels = img.shape

#----------------- Detecting Objects -----------------
blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)

net.setInput(blob)
outs = net.forward(outputlayers)

#--------------------- Showing Informations on the screen ------------

class_ids = []
confidences = []
boxes = []
for out in outs :
    for detection in out :
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.07 :
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)


            # Rectangle coordinates
            x = int(center_x - w / 2 )
            y = int(center_y - h / 2 )

            if class_id not in class_ids :
                class_ids.append(class_id)
                boxes.append([x,y,w,h])
                confidences.append(float(confidence))


indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.5,0.4)
for i in range(len(boxes)) :
    x,y,w,h = boxes[i]
    label = str(classes[class_ids[i]])
    color = colors[i]
    cv2.rectangle(img, (x , y) , (x + w , y + h) , color, 2)
    cv2.putText(img,label , (x, y + 30), cv2.FONT_ITALIC , 1, color , 3)


cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()