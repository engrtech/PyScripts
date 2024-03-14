import cv2
import numpy as np

#there to make it integer with values from 0-255 you can redefine it as np.uint8
img = np.zeros((512, 512, 3), np.uint8)
#and now they will show as int
print(img)

#draw green line from origin to the other corner...
cv2.line(img,(0, 0), (img.shape[1],img.shape[0]),(0,255,0),2)

#draw rectangle
cv2.rectangle(img, (350, 100), (450, 200), (0, 0, 255), cv2.FILLED)

#draw circle
cv2.circle(img, (100,200), 50, (255,0,0), 3)

#put text
cv2.putText(img, "Draw Shapes", (75,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,100,100))

cv2.imshow("Image", img)

cv2.waitKey(0)