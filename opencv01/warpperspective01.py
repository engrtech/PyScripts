import cv2
import numpy as np

img = cv2.imread('res/cards.jpg')

pts1 = np.array([[1135,201],[1478,366],[1001,671],[650,479]], np.float32)
w, h = 250, 350
pts2 = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
print(pts1)
print(pts2)

#get the transform matrix
matrix = cv2.getPerspectiveTransform(pts1, pts2)

#and this is what we get after transforming
output = cv2.warpPerspective(img, matrix, (w, h))

print(pts1[0][0])

for x in range(0,4):
    cv2.circle(img, (int(pts1[x][0]), int(pts1[x][1])), 5, (0,0,255.), cv2.FILLED)

cv2.imshow("Original Image ", img)
cv2.imshow("Output Image", output)
cv2.waitKey(0)