import cv2
import numpy as np

def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter == 4:
            counter = 0
            four_pts[0] = 0, 0
            four_pts[1] = 0, 0
            four_pts[2] = 0, 0
            four_pts[3] = 0, 0
        #gotta store that in the circles matrix
        four_pts[counter] = x,y
        counter = counter + 1
        print(four_pts)

path = "res/cards.jpg"
img = cv2.imread(path)

#array to store mouse clicks
four_pts = np.zeros((4, 2), np.uint16)
counter = 0

while True:
    #width and height for transformed window
    w, h = 250, 350

    if counter == 4:
        #default position of card to transform
        pts1 = np.array([four_pts[0],four_pts[1],four_pts[2],four_pts[3]], np.float32)
        pts2 = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
        #get the transform matrix
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #and this is what we get after transforming
        output = cv2.warpPerspective(img, matrix, (w, h))
        cv2.imshow("Output Image ", output)

    #for x in range(0,4):
        #cv2.circle(img, (int(four_pts[x][0]), int(four_pts[x][1])), 5, (0,0,255.), cv2.FILLED)

    cv2.imshow("Original Image ", img)


    cv2.setMouseCallback("Original Image ", mousePoints) #spell the windowname to match!!!


    cv2.waitKey(1)