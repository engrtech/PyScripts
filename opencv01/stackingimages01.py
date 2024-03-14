import cv2
import numpy as np

#numpy has horizontal and vertical stacking functions
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


#load all the images
path01 = "res/pink_ball/pb01.JPG"
path02 = "res/pink_ball/pb02.JPG"
path03 = "res/pink_ball/pb03.JPG"
path04 = "res/pink_ball/pb04.JPG"
#load them all with the same channel
img01 = cv2.imread(path01)
img02 = cv2.imread(path02)
img03 = cv2.imread(path03)
img04 = cv2.imread(path04)

#img01 = cv2.resize(img01, (0,0), None, 1, 1)
#img02 = cv2.resize(img02, (0,0), None, 1, 1)
#img03 = cv2.resize(img03, (0,0), None, 1, 1)
#img04 = cv2.resize(img04, (0,0), None, 1, 1)

#hor01 = np.hstack((img01, img02))
#ver01 = np.vstack((img01, img02))
#hor02 = np.hstack((img03, img04))
#ver02 = np.vstack((img03, img04))

#send in the scale value and image array
imgStack = stackImages(1, ([img01, img02], [img03, img04]))
cv2.imshow("Stacked Images", imgStack)

cv2.waitKey(0)