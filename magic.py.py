import cv2
import time
import numpy as np


cap=cv2.VideoCapture(0)
fourcc= cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.avi',fourcc,30, (640,480))



time.sleep(3)
count = 0
background=0

# Capturing and storing the static background frame
for i in range(60):
	ret,background = cap.read()

while(cap.isOpened()):
	ret, img = cap.read()
	if not ret:
		break
	#count+=1
	#img = np.flip(img,axis=1)
	
	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Generating mask to detect red color
	lower_red = np.array([0,120,70])
	upper_red = np.array([20,255,255])
	red_mask1 = cv2.inRange(hsv,lower_red,upper_red)

	red1 = cv2.bitwise_and(img, img, mask=red_mask1)
	
	lower_red = np.array([160,120,70])
	upper_red = np.array([180,255,255])
	red_mask2 = cv2.inRange(hsv,lower_red,upper_red)

	red2 = cv2.bitwise_and(img, img, mask=red_mask2)

	
	red_mask=red_mask1+red_mask2

	red = cv2.bitwise_and(img, img, mask=red_mask)

	kernel = np.ones((3,3), np.uint8) 
	
	red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel,iterations=2)
	red_after_open = cv2.bitwise_and(img, img, mask=red_mask)
	
	red_mask = cv2.dilate(red_mask, kernel, iterations = 1)
	red_after_open_and_dilate = cv2.bitwise_and(img, img, mask=red_mask)

	not_red_mask = cv2.bitwise_not(red_mask)
	not_red = cv2.bitwise_and(img, img, mask=not_red_mask)
	
	res1 = cv2.bitwise_and(background,background,mask=red_mask)
	res2 = cv2.bitwise_and(img,img,mask=not_red_mask)
	final_output = cv2.addWeighted(res1,1,res2,1,0)
	
	#cv2.imshow("Red", red)
	#cv2.imshow("Red after Open", red_after_open)
	#cv2.imshow("Red after open and dilate",red_after_open_and_dilate )
	#cv2.imshow("Final", not_red)
	#cv2.imshow("res1",res1)
	#cv2.imshow("res2",res2)
	cv2.imshow("Awesome right...!!!",final_output)
	if cv2.waitKey(1)==ord('q'):
		break