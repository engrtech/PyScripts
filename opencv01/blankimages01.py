import cv2
import numpy as np

#black 512x512 size. it is a 1 channel color
img = np.zeros((512,512))
#printing img will show you that the values are 1 channel
print(img)

#to make it three channel...
img = np.zeros((512, 512, 3))
#printing img will show you that the values are float and three channel
print(img)

#there to make it integer with values from 0-255 you can redefine it as np.uint8
img = np.zeros((512, 512, 3), np.uint8)
#and now they will show as int
print(img)

cv2.imshow("Image", img)

cv2.waitKey(0)