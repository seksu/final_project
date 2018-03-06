#created by sek su
import cv2

minCascade      = 1.05
maxCascade      = 5

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')

cap = cv2.VideoCapture('http://admin:01290129@192.168.1.220/video1.mjpg')

while 1:
	ret, frame = cap.read()
	#faces = face_cascade.detectMultiScale(img, minCascade, maxCascade) #1.3 5
	#for (x,y,w,h) in faces:
	#	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	#	cv2.putText(img,'face',(x-3,y-3), font, w*h/60000,(255,0,0),2)
	#	cv2.imshow('img',img)
	print(ret)
	cv2.imshow('frame',frame)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()