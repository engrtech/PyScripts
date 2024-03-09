#simplest method is using the gaussian method

import cv2
import numpy as np

kernel = np.ones((5,5), np.uint16)
print(kernel)

path = "res/pink_ball/pb01.JPG"

#flag 0 will convert it to grayscale for image in the imread function.
img = cv2.imread(path)
#but it is better to do it this way...
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#now we use a gaussian filter
img_blur = cv2.GaussianBlur(img_gray,(5,5), 0)

#now detect edge
img_canny = cv2.Canny(img_blur, 200, 200)

#dilation #mess with the iterations
img_dilation = cv2.dilate(img_canny,kernel, iterations=2)

#erosion #mess with the iterations
img_erosion= cv2.erode(img_dilation, kernel, iterations=1)


cv2.imshow("pb01window",img)
cv2.imshow("pb01_canny_window",img_canny)
cv2.imshow("pb01_dil_window", img_dilation)
cv2.imshow("pb01_erode_window", img_erosion)
cv2.waitKey(0)