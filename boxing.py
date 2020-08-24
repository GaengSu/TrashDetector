from mtcnn import MTCNN
import cv2
from pascal_voc_writer import Writer

#파일 불러오기

for i in range(229):
    filename = "C:/Users/wkdru/PycharmProjects/mtcnn_test/images/JKS/JKS{0}".format(i)
#이미지 읽기
    img = cv2.cvtColor(cv2.imread(filename+'.jpg'), cv2.COLOR_BGR2RGB)
    detector = MTCNN()                                                      #mtcnn 객체 생성
    result = detector.detect_faces(img)                                     #이미지에서 얼굴 labeling

    writer = Writer(filename+'.jpg', img.shape[1], img.shape[0])            #labeling한 이미지 정보 가져오기 path,width,height

    writer.addObject('JKS', result[0]['box'][0],                            #class name, xmin, ymin,xmax,ymax
                     result[0]['box'][1],
                     result[0]['box'][0] + result[0]['box'][2],
                     result[0]['box'][1] + result[0]['box'][3])

    writer.save(filename + '.xml')

