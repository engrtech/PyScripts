import cv2
import numpy as np

img = cv2.imread('res/cards.jpg')

cv2.imshow("Original Image ", img)
cv2.waitKey(0)