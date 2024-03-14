import cv2

#in opencv the positive is the 4th quadrant
path = "res/pink_ball/pb01.JPG"

img = cv2.imread(path)
#now output the size of the image in ROWS, COLUMNS...
print(img.shape)

#for resizing IT IS WIDTH, HEIGHT
width, height = 600, 400
imgResized = cv2.resize(img, (width, height))
#confirm that the new size is different
print(imgResized.shape)

cv2.imshow("PinkBall Original", img)
cv2.imshow("PinkBall Resized", imgResized)

#cop it but this time height comes first! BECAUSE ROWS!
imgCropped = img[200:640, 0:480]
print(imgCropped.shape)
cv2.imshow("PinkBall Cropped", imgCropped)

cv2.waitKey(0)