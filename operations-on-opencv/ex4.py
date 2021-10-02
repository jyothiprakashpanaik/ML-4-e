# moving object detection
import cv2
import imutils
import time
cam = cv2.VideoCapture(0)
time.sleep(1)

firstframe = None
area = 5000

while True:
	_,img = cam.read()
	text = "Normal"
	img = imutils.resize(img,width=500)
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gaussianImg = cv2.GaussianBlur(grayImg,(21,21),0)
	if firstframe is None:
		firstframe = gaussianImg
		continue

	
	imgDiff = cv2.absdiff(firstframe, grayImg)
	threshImg = cv2.threshold(imgDiff,  100, 255, cv2.THRESH_BINARY)[1]
	threshImg = cv2.dilate(threshImg,None,iterations=2)

	cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	cnts = imutils.grab_contours(cnts)

	for c in cnts:
		if cv2.contourArea(c) < area:
			continue
		(x,y,w,h) = cv2.boundingRect(c)
		cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255),3)
		text = "Moving object detected"

	print(text)
	if text == "Normal":
		cv2.putText(img, text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
	else:
		cv2.putText(img, text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

	cv2.imshow("camraFeed", img)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break



cam.release()

cv2.destroyAllWindows()