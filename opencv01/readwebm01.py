import cv2

#it would be ideal to match the accepted webcam specs
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture("res/testvid01.webm") #an example to open a specific file
#cap = cv2.VideoCapture(0)
#let's define the framewidth and height to the camera.
#cap.set(3,frameWidth) #3 is set as width in opencv
#cap.set(4,frameHeight) #4 is set as the height in opencv

while True:
    success, img = cap.read() #it reads from the capture and stores it in an image. success is a bool
    #if it can successfully read then it is True, if it cannot then it will be false
    #we can resize it here if we need it to
    img = cv2.resize(img, (frameWidth, frameHeight))
    img = cv2.imshow("video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'): #if Q is pressed then it will break the loop?
        break