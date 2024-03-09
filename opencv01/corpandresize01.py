import cv2

#in opencv the positive is the 4th quadrant

path = "res/pink_ball/pb01.JPG"

img = cv2.imread(path)
print(img.shape)

width, height =
imgResize = cv2.resize(img, (width, height))

cv2.imshow("Road", img)

