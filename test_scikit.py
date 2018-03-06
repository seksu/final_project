#test sek su
import cv2
cam = cv2.VideoCapture('/home/pansek/workspace/source/vdo.mp4')
ret_val, img = cam.read()

print(ret_val)
while(True):
	if(ret_val == True):
	    cv2.imshow('my webcam', img)
	    if cv2.waitKey(100) == 27:
	       break  # press 'esc' for quit
