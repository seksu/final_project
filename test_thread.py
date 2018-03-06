import threading
import os
import imageio
import cv2
import time
import numpy as np
import sys
import dlib
from skimage import io


videoPath 		= 'video/'
previousVideo 	= None

fail = 0
minCascade      = 1.05
maxCascade      = 5
offset          = 50
facecount = 0
kernel = np.ones((5,5),np.uint8)

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
fgbg = cv2.createBackgroundSubtractorMOG2(history=1800, varThreshold=20, detectShadows=0)
detector = dlib.get_frontal_face_detector()



def faceFind(vi,i):
	print("process : " + str(i))

	image = vi.get_data(i)
	bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	fgmask = fgbg.apply(bgr_image)
	opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

	ret,thresh = cv2.threshold(closing,50,255,0)
	im2,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	if(contours):
		print("having contour")
		maxx = 1279
		maxy = 719
		maxw = 1
		maxh = 1
		for contour in contours:
			if(cv2.contourArea(contour) > 400):
				xb,yb,wb,hb = cv2.boundingRect(contour)
				if(xb < maxx):
					maxx = xb
				if(yb < maxy):
					maxy = yb
				if(wb > maxw):
					maxw = wb
				if(hb > maxh):
					maxh = hb
				if((xb-maxx) > maxw):
					maxw = (xb-maxx)+wb
				if((yb-maxy) > maxh):
					maxh = (yb-maxy)+hb
				if((maxx+maxw) > 1280):
					maxx = 0
					maxw = 1280
				if((maxy+maxh) > 720):
					maxy = 0
					maxh = 720
		#cv2.rectangle(bgr_image,(maxx,maxy),(maxx+maxw,maxy+maxh),(0,0,255),4)
		#cv2.imshow('process',image)
		dets = detector(image, 1)
		if(len(dets)):
			print("Number of faces detected: {}".format(len(dets)))
			for i, d in enumerate(dets):
				print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))
				cv2.imwrite('face/face_'+str(facecount)+'.jpg',bgr_image[d.top():d.bottom(),d.left():d.right()])
				facecount = facecount+1
	return


videoList = os.listdir(videoPath)
for videoName in videoList:
	print("processing : "+str(videoName))
	f = open('listProcess','wb')
	print(f.read())
	f.write("this msg/n")
	f.close
	try:
		vid = imageio.get_reader(str(videoPath)+str(videoName),  'ffmpeg')
	except Exception as inst:
		fail += 1
		print("Some reader error")
		continue
	
	for i in range(300):
		try:
			t = threading.Thread(target=faceFind, args=(vid,i))
			t.start()


				# faces = face_cascade.detectMultiScale(bgr_image[maxy:maxy+maxh,maxx:maxx+maxw], minCascade, maxCascade) #1.3 5
				# for (x,y,w,h) in faces:
				# 	print('face find!')
				#  	cv2.imwrite('face/face_'+str(facecount)+'.jpg',bgr_image[y+maxy:y+h+maxy,x+maxx:x+w+maxx])
				#  	cv2.rectangle(bgr_image,(x+maxx,y+maxy),(x+maxx+w,y+maxy+h),(255,0,0),2)
				#  	facecount = facecount+1

		except Exception as inst:
			fail += 1
			print("processing error : "+str(inst))
			#print(type(image))
			continue
		#cv2.imshow('image',image)
		#cv2.waitKey(1)
	print("end processing : "+str(videoName))
	# if(previousVideo):
	#os.remove(str(videoPath)+videoName) # for delete file
	# previousVideo = videoName
print('fail : '+str(fail))
cv2.waitKey(1)
cv2.destroyAllWindows()

