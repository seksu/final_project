#created by sek su
import os
import imageio
import cv2
import time
import numpy as np
import sys
import dlib
from skimage import io
from datetime import datetime

videoPath 		= 'video/'
previousVideo 	= None

fail = 0
minCascade      = 1.05
maxCascade      = 5
offset          = 50
facecount = 0
kernel = np.ones((5,5),np.uint8)

body_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
fgbg = cv2.createBackgroundSubtractorMOG2(history=1800, varThreshold=20, detectShadows=0)
detector = dlib.get_frontal_face_detector()

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

frameShirt = 	[[0.33,0.25],[0.42,0.25],[0.50,0.25],[0.58,0.25],[0.66,0.25],
				[0.50,0.20],[0.50,0.31],[0.50,0.37],[0.50,0.43],[0.50,0.49]]

#videoList = os.listdir(videoPath)
f = open('downloadList','r')
lines = f.readlines()

for videoName in lines:
	bodyCount = 0
	faceCount = 0
	testCount = 0

	print("processing : "+str(videoName))
	f = open('processList','ab+')
	inLine = False
	for line in f:
		#print('line : ' + str(len(line)))
		#print('videoName : ' + str(len(videoName+'\n')))
		if(line == (videoName)):
			print('inLine is True')
			inLine = True
			break
	if(inLine):
		continue
	else:
		f.write(videoName)

	f.close()
	try:
		videoName = videoName.replace("\n","")
		print("try : "+str(videoPath)+str(videoName))
		vid = imageio.get_reader(str(videoPath)+str(videoName),  'ffmpeg')
	except Exception as inst:
		fail += 1
		print("Some reader error : "+str(inst))
		continue
	for i in range(300):
		print("process : " + str(i))
		try:							# processing
			image = vid.get_data(i)
			bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			fgmask = fgbg.apply(bgr_image)
			opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
			closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

			ret,thresh = cv2.threshold(closing,50,255,0)
			im2,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

			if(contours):
				fileName = videoName.replace(".avi","")
				#print("having contour")
				maxx = 1279
				maxy = 719
				maxw = 1
				maxh = 1
				for contour in contours:

					if(cv2.contourArea(contour) > 400):
						print("having contour")
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

						roi_image = bgr_image[maxy:maxy+maxh,maxx:maxx+maxw]
						rgb_roi_image = image[maxy:maxy+maxh,maxx:maxx+maxw]
						#cv2.imwrite('testbody/test'+str(fileName)+str(testCount)+'.jpg',roi_image)
						#testCount += 1

				#cv2.rectangle(bgr_image,(maxx,maxy),(maxx+maxw,maxy+maxh),(0,0,255),4)
				#cv2.imshow('process',image)

						print("face det")
						face_path = None
						position_x = None
						position_y = None
						position_w = None
						position_h = None

						dets = detector(image, 1)
						if(len(dets)):

							print("Number of faces detected: {}".format(len(dets)))
							for i, d in enumerate(dets):
								print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))
								position_x = d.left()
								position_y = d.top()
								position_w = d.right()-d.left()
								position_h = d.bottom()-d.top()
								face_path = 'face/face_'+str(fileName)+str(faceCount)+'.jpg'
								cv2.imwrite('face/face_'+str(fileName)+str(faceCount)+'.jpg',bgr_image[d.top():d.bottom(),d.left():d.right()])
								faceCount = faceCount+1

				# bodys = body_cascade.detectMultiScale(image, minCascade, maxCascade) #1.3 5
				# bodyCount = 0
				# for (x,y,w,h) in bodys:
				# 	print('body detect')
				#  	cv2.imwrite('body/body_'+str(fileName)+str(bodyCount)+'.jpg',image[y:y+h,x:x+w])
				#  	bodyCount = bodyCount+1

						print("body det")
						fullbody_path = None
						bodys,w=hog.detectMultiScale(roi_image, winStride=(8,8), padding=(32,32), scale=1.05)

						maxSize = 0
						pos_body_x = 0
						pos_body_y = 0
						pos_body_w = 0
						pos_body_h = 0

						shirtcolor_r = None
						shirtcolor_g = None
						shirtcolor_b = None

						for x, y, w, h in bodys:
							if(w*h > maxSize):
								maxSize = w*h

						for x, y, w, h in bodys:
							if(w*h >= maxSize):
								print('body detect')
								fullbody_path = 'body/body_'+str(fileName)+str(bodyCount)+'.jpg'
								cv2.imwrite('body/body_'+str(fileName)+str(bodyCount)+'.jpg',bgr_image[y+maxy:y+h+maxy,x+maxx:x+w+maxx])
								bodyCount = bodyCount+1
								pos_body_x = x
								pos_body_y = y
								pos_body_w = w
								pos_body_h = h
								list_B = []
								list_G = []
								list_R = []

								for x,y in frameShirt:
									list_B.append(image[pos_body_y+int(y*pos_body_h),(pos_body_x+int(x*pos_body_w)),0])
									list_G.append(image[pos_body_y+int(y*pos_body_h),(pos_body_x+int(x*pos_body_w)),1])
									list_R.append(image[pos_body_y+int(y*pos_body_h),(pos_body_x+int(x*pos_body_w)),2])

								shirtcolor_r = int(np.average(list_R))
								shirtcolor_g = int(np.average(list_G))
								shirtcolor_b = int(np.average(list_B))

								sd_r 	= int(np.std(list_B))
								sd_g	= int(np.std(list_G))
								sd_b 	= int(np.std(list_R))


#/////////////////////////// For Database //////////////////////////////////

						dt_str 			= fileName[10:12]+'/'+fileName[8:10]+'/'+fileName[4:8]+' '+fileName[12:14]+':'+fileName[14:16]+':'+fileName[16:18]
						timestamp 		= datetime.strptime(dt_str, '%d/%m/%Y %I:%M:%S') #time + date
						face_path 		= face_path
						fullbody_path 	= fullbody_path
						videopath 		= 'video/'+videoName
						timelapse 		= i
						position_x 		= position_x
						position_y 		= position_y
						position_w 		= position_w
						position_h 		= position_h
						shirtcolor_r 	= shirtcolor_r
						shirtcolor_g 	= shirtcolor_g
						shirtcolor_b 	= shirtcolor_b
						sd_r 			= sd_r
						sd_g 			= sd_g
						sd_b 			= sd_b


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

#end
