#simplest method is using the gaussian method

import cv2

path = "res/pink_ball/pb01.JPG"

#flag 0 will convert it to grayscale for image in the imread function.
img = cv2.imread(path)
#but it is better to do it this way...
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#now we use a gaussian filter
img_blur = cv2.GaussianBlur(img_gray,(5,5), 0)

cv2.imshow("pb01window",img)
cv2.imshow("pb01_gray_window",img_blur)
cv2.waitKey(0)