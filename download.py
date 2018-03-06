# For system_test
## By sek su

############### CONFIG ##############

ftpAddr 	= '161.246.5.152'
ftpUser		= 'root'
ftpPass	 	= '123456'
ftpDir		= 'ipcam'
tokens		= ['a121','a122','a123']

#####################################

import pylab
import cv2
#import imageio
from time import gmtime
from ftplib import FTP
from urllib import urlretrieve
from urllib import urlcleanup
import os
import time
from os.path import join, getsize

minStore 	 		= ''
listFileName 		= [] 
previousVideo_name 	= ''

while 1:
	ftp = FTP(ftpAddr)     							
	ftp.login(ftpUser,ftpPass)

	year 	= str(gmtime().tm_year)

	if(gmtime().tm_mon < 10):
		month 	= '0'+str(gmtime().tm_mon)
	else:
		month 	= str(gmtime().tm_mon)

	if(gmtime().tm_mday < 10):
		day 	= '0'+str(gmtime().tm_mday)
	else:
		day 	= str(gmtime().tm_mday)

	if(((gmtime().tm_hour+7)%24) < 10):
		hour 	= '0'+str((gmtime().tm_hour+7)%24)
	else:
		hour 	= str((gmtime().tm_hour+7)%24)

	if(((gmtime().tm_min-3)%60) < 10):
		minute 	= '0'+str((gmtime().tm_min-1)%60)
	else:
		minute 	= str((gmtime().tm_min-3)%60)

	if((gmtime().tm_sec) < 10):
		sec 	= '0'+str(gmtime().tm_sec)
	else:
		sec 	= str(gmtime().tm_sec)

	minStore = minute

	ftp.cwd("/ipcam/"+year+""+month+""+day+"/"+hour+"00/")
	currentPath = ftp.nlst()
	#print("/ipcam/"+year+""+month+""+day+"/"+hour+"00/")

	for filename_video in currentPath:
		#print(filename_video)
		#print(token+year+month+day+hour+minStore)
		for token in tokens:
			if(filename_video.startswith(token+year+month+day+hour+minStore) and filename_video.endswith(".avi")):
				non = True
				for name in listFileName:
					if(filename_video == name):
						non = False
				if(non == True):
					listFileName.append(filename_video)
					# if(previousVideo_name):
					# 	file = open("video/"+previousVideo_name, 'rb')
					# 	print("previous size : "+file)
					print(filename_video)
					urlcleanup()
					urlretrieve("ftp://"+ftpUser+":"+ftpPass+"@"+ftpAddr+"/ipcam/"+year+""+month+""+day+"/"+hour+"00/"+str(filename_video),"video/"+str(filename_video))
					previousVideo = "/ipcam/"+year+""+month+""+day+"/"+hour+"00/"+str(filename_video)
					previousVideo_name = str(filename_video)
					f = open('downloadList','a+')
					f.write(filename_video+'\n')
					f.close
					time.sleep(1)
					print("Download complete")
				if(minStore != minute):
					minStore = minute
					listFileName = []
	time.sleep(1)

#urlretrieve("ftp://"+ftpUser+":"+ftpPass+"@"+ftpAddr+"/ipcam/"+year+""+mouth+""+day+"/"+hour+"00/"+token+""+year+""+mouth+""+hour+,"source/input.avi")

#filename = '/home/pansek/workspace/source/input.avi'
#vid = imageio.get_reader(filename,  'ffmpeg')

#image = vid.get_data(100)

#rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# print(year)
# print(month)
# print(day)
# print(hour)
# print(minute)
# print(sec)


# cv2.waitKey(0)
# cv2.destroyAllWindows()