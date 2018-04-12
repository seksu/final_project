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
import subprocess


sys.path.append('/home/pansek/webserver')
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'webserver.settings'
django.setup()
from source.models import Searching_Detail
from account.models import Account
from camera.models import Camera_Detail
from django.core.cache import cache


debugMode = True

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

def facerecognition(image):
	temp    = subprocess.check_output(['python', '/home/pansek/openface/demos/classifier.py', 'infer', 'classifier.pkl', image])
	lines   = temp.split("\n")
	lineEnd = str(lines[len(lines)-2])
	words   = lineEnd.split(' ')
	if(words[0] == "Predict"):
		print("start with predict")
		print("Name : "+words[1])
		return(words[1])
	else:
		print("doesn't start with predict")
		return words[1]
	print(":: " + lineEnd)

#videoList = os.listdir(videoPath)
f = open('downloadList','r')
lines = f.readlines()
count_frame = 0
for videoName in lines:
	bodyCount = 0
	faceCount = 0
	testCount = 0
	index = 0
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
		#fail += 1
		print("Some reader error : "+str(inst))
		continue
	for Tlapse in range(300):
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
				if(debugMode):
					print("length of contour : "+str(len(contours)))
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
						face_path 			= None
						position_x 			= None
						position_y 			= None
						position_w 			= None
						position_h 			= None
						recognition_face	= None

						dets = detector(image, 1)
						if(len(dets)):

							print("Number of faces detected: {}".format(len(dets)))
							for i, d in enumerate(dets):
								print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))
								position_x 			= d.left()
								position_y 			= d.top()
								position_w 			= d.right()-d.left()
								position_h 			= d.bottom()-d.top()
								face_path 			= 'face/face_'+str(fileName)+str(faceCount)+'.jpg'
								cv2.imwrite('face/face_'+str(fileName)+str(faceCount)+'.jpg',bgr_image[d.top():d.bottom(),d.left():d.right()])
								faceCount 			= faceCount+1
								recognition_face 	= facerecognition(face_path)

				# bodys = body_cascade.detectMultiScale(image, minCascade, maxCascade) #1.3 5
				# bodyCount = 0
				# for (x,y,w,h) in bodys:
				# 	print('body detect')
				#  	cv2.imwrite('body/body_'+str(fileName)+str(bodyCount)+'.jpg',image[y:y+h,x:x+w])
				#  	bodyCount = bodyCount+1

						print("body det")
						fullbody_path = None
						bodys,w=hog.detectMultiScale(roi_image, winStride=(8,8), padding=(16,16), scale=1.1)
						print("pass0")
						maxSize = 0
						pos_body_x = None
						pos_body_y = None
						pos_body_w = None
						pos_body_h = None

						shirtcolor_r = None
						shirtcolor_g = None
						shirtcolor_b = None

						sd_r = None

						for x, y, w, h in bodys:
							if(w*h > maxSize):
								maxSize = w*h
						print("pass1")

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
						print("pass2")

#/////////////////////////// For Database ///////////////////////////////////

						tokens = fileName[0:8];

						dt_str 				= fileName[14:16]+'/'+fileName[12:14]+'/'+fileName[8:12]+' '+fileName[16:18]+':'+fileName[18:20]+':'+fileName[20:22]
						account = Account.objects.filter(email=recognition_face).first()
						camera = Camera_Detail.objects.filter(token=tokens).first()


						search = Searching_Detail.objects.create(
							timestamp = datetime.strptime(dt_str, '%d/%m/%Y %H:%M:%S'), #time + date
							face_path = face_path,
							fullbody_path = fullbody_path,
							video_path = 'video/'+videoName,
							timelapse = Tlapse,
							position_x = position_x,
							position_y = position_y,
							position_w = position_w,
							position_h = position_h,
							pos_body_x = pos_body_x,
							pos_body_y = pos_body_y,
							pos_body_w = pos_body_w,
							pos_body_h = pos_body_h,
							shirtcolor_r = shirtcolor_r,
							shirtcolor_g = shirtcolor_g,
							shirtcolor_b = shirtcolor_b,
							sd_r = sd_r,
							sd_g = sd_g,
							sd_b = sd_b,
							account = account,
							camera = camera
						)
						search.save()
						if search.account:
							if search.account.email == "unknown@"+cache.get('company')+".com":
								cache.set(str(index),search,60)
								cache.set('index',index,60*60*24)
								index+=1
						print('>>>>> frame : '+ str(count_frame) +'<<<<<')
						count_frame += 1
						#print("facepath" + str(face_path))
						#print("fullbody" + str(fullbody_path))



		except Exception as inst:
			#fail += 1
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
