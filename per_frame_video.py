import cv2


cap = cv2.VideoCapture('JKS.mp4')

count = 0

while (cap.isOpened()):
    ret, image = cap.read()

    cv2.imwrite("images/jks/jks%d.jpg" % count, image)
    print('Saved frame%d.jpg' % count)
    count += 1

cap.release()
