import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

returnlist = []
trashlist = [0,0,0,0,0]
count = 0

classes = ['cardboard/paper','glass','metal','plastic','trash']

def trashfunc():

    net = cv2.dnn.readNet("p2_30000.weights", "p2.cfg")

    layer_names = cv2.net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in cv2.net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    cap = cv2.VideoCapture(0)

    while(True):
        if count == 20:
            count = 0
            break
        ret, frame = cap.read()
        if cv2.waitKey(1) == ord('q'):
            break
        if(ret):
            cv2.imshow("Image", frame)

            height, width, channels = frame.shape

            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            cv2.net.setInput(blob)
            outs = cv2.net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.4)

            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), font, 1, color, 2)
                    print(label, confidences[i], x, y, w, h)
                    cv2.imshow("detect", frame)
                    if label == classes[0]:
                        trashlist[0] = trashlist[0] + 1
                    elif label == classes[1]:
                        trashlist[1] = trashlist[1] + 1
                    elif label == classes[2]:
                        trashlist[2] = trashlist[2] + 1
                    elif label == classes[3]:
                        trashlist[3] = trashlist[3] + 1
                    elif label == classes[4]:
                        trashlist[4] = trashlist[4] + 1
                    count = count + 1
    cap.release()
    cv2.destroyAllWindows()

    return trashlist

