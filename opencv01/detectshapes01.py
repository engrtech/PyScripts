#1. creating a simple image stack with img, imgBlur, and imgGray
#2. then create a trackbar for threshold
#3. then do a canny image
#4. then dilate with a 5,5 kernel

import cv2
import numpy as np
import cv2utils

def empty(a): #called whenever there is a change in the value. but there won't be any right now
    pass

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 2500:
            cv2.drawContours(imgContour, contours, -1, (255, 0, 255), 5)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True) #0.02*peri is resolution...
            print(approx) #gives points of the
            x, y, w, h = cv2.boundingRect(approx) #capture the corners
            cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 5) #draw the rect boundingbox
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Points: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)


#start
w, h = 640, 480

cap = cv2.VideoCapture(0) #this begins the video capture.
cap.set(3, w) #set the width
cap.set(4, h) #set the

#create trackbar
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 150,255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 255,255, empty)

while True:
    _, img = cap.read() #we dont care about the success of read. it will read.

    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY) #remember this is not 3 channel
                                                        #but it does not matter if we use the StackImages function

    #read whatever has been selected by the user.
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)


    getContours(imgDil, imgContour)

    #display images stacked. see stackimages01.py
    imgStack = cv2utils.stackImages(1,      ([img, imgGray, imgCanny],
                                                            [imgDil, imgContour,imgContour]))
    cv2.imshow("ImageStack", imgStack)

    #quit command. always last.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()