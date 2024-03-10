import cv2
import numpy as np

#there to make it integer with values from 0-255 you can redefine it as np.uint8
img = np.zeros((512, 512, 3), np.uint8)
#and now they will show as int
print(img)

#BGR (alphabetical in python?)
img[:] = 255, 0, 0
#the colon changes the color everywhere

cv2.imshow("Image", img)

cv2.waitKey(0)