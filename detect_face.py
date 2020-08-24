#############################################
# Refering to some code of darknet repository#
#############################################

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import requests

classes = ['KEC', 'PSI', 'SJS', 'SSJ', 'AJH',
           'YSS', 'LSH', 'LJH', 'LJY', 'JKS', 'JKY', 'JSY', 'CDW']

net = cv2.dnn.readNet("yolov3-tiny-face_109000.weights",
                      "yolov3-tiny-face.cfg")
returnlist = []
facelist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def facefunc():
    count = 0

    cap = cv2.VideoCapture('http://name:pass@192.168.43.27:8080/video')  # ip,계정,비밀번호
    cap.set(3, 480)
    cap.set(4, 320)
    width = int(cap.get(3))
    height = int(cap.get(4))

    now = time.time()
    count = 0

    fps = 60
    fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = []
    for i in range(100):
        a = str(i) + '.avi'
        out.append(cv2.VideoWriter(a, fcc, fps, (width, height)))

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # cap = cv2.VideoCapture(0)

    while (True):
        if count == 20:
            count = 0
            break
        ret, frame = cap.read()
        if cv2.waitKey(1) == ord('q'):
            break
        if (ret):
            # cv2.imshow("Image", frame)

            height, width, channels = frame.shape

            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # 이미지 blob함수로 전처리
            net.setInput(blob)  # 후에 forward pass진행
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]  # 클래스 id 및 신뢰도 구하기
                    class_id = np.argmax(scores)  # argmax를 통해 one hot encoding
                    confidence = scores[class_id]  # 해당 신뢰드

                    if confidence > 0.1:  # 해당 신뢰도 10%이상인 경우    #########이부분 파라미터 수정 고려하기
                        center_x = int(detection[0] * width)  # boxing update해주기        #########
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)  # 사각형
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
                    # cv2.imshow("detect", frame)
                    count = count + 1
                    if label == classes[0]:
                        facelist[0] = facelist[0] + 1
                    elif label == classes[1]:
                        facelist[1] = facelist[1] + 1
                    elif label == classes[2]:
                        facelist[2] = facelist[2] + 1
                    elif label == classes[3]:
                        facelist[3] = facelist[3] + 1
                    elif label == classes[4]:
                        facelist[4] = facelist[4] + 1
                    elif label == classes[5]:
                        facelist[5] = facelist[5] + 1
                    elif label == classes[6]:
                        facelist[6] = facelist[6] + 1
                    elif label == classes[7]:
                        facelist[7] = facelist[7] + 1
                    elif label == classes[8]:
                        facelist[8] = facelist[8] + 1
                    elif label == classes[9]:
                        facelist[9] = facelist[9] + 1
                    elif label == classes[10]:
                        facelist[10] = facelist[10] + 1
                    elif label == classes[11]:
                        facelist[11] = facelist[11] + 1
                    elif label == classes[12]:
                        facelist[12] = facelist[12] + 1
    cap.release()
    cv2.destroyAllWindows()
    return facelist

