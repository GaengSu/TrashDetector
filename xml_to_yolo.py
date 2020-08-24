import xml.etree.ElementTree as ET
import os
import cv2

nc = open("100/class.names")                        #class name 가져오기
name_class = dict()
for idx, i in enumerate(nc):                        #class들 배열에 input
    name_class[i.replace('\n','')] = str(idx)
pathes = "100/"                                     #setting 경로
rr = open(pathes + 'train.txt','w')
for path, dir, apple in os.walk(pathes):
    if len(dir)>0:
        continue
    folderList = os.listdir(path)
    print(path)
    path = path + '/'
    r = open(path + 'train.txt','w')
    for i in folderList :
        print(i)
        if i.split('.')[1] == 'jpg':
            r.write(path + i)
            rr.write(path + i)
            r.write('\n')
            rr.write('\n')
            continue

        if i.split('.')[1] == 'xml':
            tree = ET.parse(path+i)
            root = tree.getroot()

            img = cv2.imread(path+i.split('.')[0] + '.jpg')
            width = img.shape[1]
            height = img.shape[0]

            width2 = int(root.find('size').find('width').text)
            height2 = int(root.find('size').find('height').text)

            if not width == width2:
                print(i)

            #print(i)
            f = open(path+i.split('.')[0] + '.txt','w')
            for j in root.iter(tag = 'object'):
                label_text = j.find('name').text

                f.write(name_class[label_text])

                f.write(' ')

                xmin = int(j.find('bndbox').find('xmin').text)
                xmax = int(j.find('bndbox').find('xmax').text)
                ymin = int(j.find('bndbox').find('ymin').text)
                ymax = int(j.find('bndbox').find('ymax').text)

                f.write(str(round(((xmin + xmax) / 2) / width,5)))
                f.write(' ')

                f.write(str(round(((ymin + ymax) / 2) / height,5)))
                f.write(' ')

                f.write(str(round(((xmax - xmin)) / width,5)))
                f.write(' ')

                f.write(str(round(((ymax - ymin)) / height,5)))
                f.write('\n')