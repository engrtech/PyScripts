import cv2

pb01 = cv2.imread("res/pink_ball/pb01.JPG") #read img

cv2.imshow("pb01windowname", pb01) #display image

cv2.waitKey(1000) #wait so we can see it. time is in ms. 0 is infinity.