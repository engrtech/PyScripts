import cv2
import numpy as np

w, h = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

def empty(a):
    pass

#create a new window to introduce these new trackbars
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0,179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179,179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0,255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255,255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0,255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255,255, empty)

while True:
    _, img = cap.read() #we dont care about the success of read. it will read.
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to another format that is easier to work with.

    #Get the user input from the GUI
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min, h_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    #the mast is the area that satisfied or falls in the specified ranges
    mask = cv2.inRange(imgHsv, lower, upper)

    #use mask to output final result of our object
    result = cv2.bitwise_and(img, img, mask = mask)

    #now we display that result as a horizontal stack
    hStack = np.hstack([img, result])

    #mask is not 3 channel so we need to convert it
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    #we can comment out individual windows...
    #cv2.imshow("Original", img)
    #cv2.imshow("HSV Color Space", imgHsv)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Result", result)

    cv2.imshow("Horizontal Stacking", hStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()