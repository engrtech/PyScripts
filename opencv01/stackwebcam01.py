#this program will take webcam input. it will process it in multiple ways.
#it will stack them. to exit hit Q

import cv2
import numpy as np
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

#it would be ideal to match the accepted webcam specs
frameWidth = 640
frameHeight = 480

#cap = cv2.VideoCapture("res/testvid01.webm") an example to open a specific file
vidcap = cv2.VideoCapture(0)
#let's define the framewidth and height to the camera.
vidcap.set(3,frameWidth) #3 is set as width in opencv
vidcap.set(4,frameHeight) #4 is set as the height in opencv

while True:
    success, cap = vidcap.read()  # it reads from the capture and stores it in an image. success is a bool
    # if it can successfully read then it is True, if it cannot then it will be false
    cv2.imshow("video", cap)  # we can resize it here if we need it to
    #img_blank = np.zeros((640, 480, 3), np.uint8)

    kernel = np.ones((5,5), np.uint8)
    print(kernel)

    cap_gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    # now we use a gaussian filter
    cap_blur = cv2.GaussianBlur(cap_gray, (5, 5), 0)

    # now detect edge
    cap_canny = cv2.Canny(cap_blur, 200, 200)

    # dilation #mess with the iterations
    cap_dilation = cv2.dilate(cap_canny, kernel, iterations=2)

    # erosion #mess with the iterations
    cap_erosion = cv2.erode(cap_dilation, kernel, iterations=1)

    imgStack = stackImages(1, ([cap, cap_gray], [cap_canny, cap_dilation]))
    cv2.imshow("Stacked Images", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'): #if Q is pressed then it will break the loop?
        break