# Real time object detection dnn
import numpy as np
import imutils
import cv2
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# prototxt = './MobileNetSSD_deploy.prototxt.txt'
# model = './MobileNetSSD_deploy.caffemodel'
confThresh = 0.2

CLASSES = ['background','aeroplane','bicycle','bird','boat',
		   'bottle','bus','car','cat','chair','cow','diningtable',
		   'dog','horse','motorbike','person','pottedplant','sheet',
		   'sofa','train','tvmonitor']
COLORS = np.random.uniform(0,255,size=(len(CLASSES),3))

print('Loading model...')
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
print('Model Loaded')
print('Straing Camera Feed...')
cam = cv2.VideoCapture(0)
time.sleep(2.0)



while True:
	_,frame = cam.read()
	frame = imutils.resize(frame,width=500)

	(h,w) = frame.shape[:2]
	imResizeBlod = cv2.resize(frame, (300,300))
	blob = cv2.dnn.blobFromImage(imResizeBlod,0.007843,(300,300),127.5)


	net.setInput(blob)
	detections = net.forward()

	detShape = detections.shape[2]
	for i in np.arange(0,detShape):
		confidence = detections[0,0,i,2]
		if  confidence > confThresh:
			idx=int(detections[0,0,i,1])
			# print('ClassID:',detections[0,0,i,1])
			box = detections[0,0,i,3:7] * np.array([w,h,w,h])
			(startX,startY,endX,endY) = box.astype('int')

			label = "{}: {:.2f}%".format(CLASSES[idx],
					 confidence * 100)
			cv2.rectangle(frame, (startX,startY), (endX,endY), COLORS[idx],2)
			if startY - 15 > 15:
				y = startY - 15
				# print(y)
			else:
				startY + 15
				y = startY
			cv2.putText(frame, label, (startX,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		print("quit")
		break
cam.release()
cv2.destroyAllWindows()