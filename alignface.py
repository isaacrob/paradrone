import cv2
import numpy as np
facefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
eyefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_eye.xml")
nosefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_mcs_nose.xml")
while not raw_input("find and align face? y/n ")=='n':
	print "finding faces..."
	cam=cv2.VideoCapture(0)
	retval,img=cam.read()
	if not retval:
		print "could not read image"
	cam.release()
	dims=facefinder.detectMultiScale(img,1.1,4,1,(20,20),img.shape[:2])
	print dims
	if len(dims)>0:
		sizelist=[w for (x,y,h,w) in dims]
		maxsize=max(sizelist)
		biggestface=[[x,y,h,w] for (x,y,h,w) in dims if w==maxsize and w>60]
		print biggestface
		if len(biggestface)>0:
			print "finding facial features..."
			for (x,y,h,w) in biggestface:
				thisface=img[x:(x+w),y:(y+h),:]
			eyes=eyefinder.detectMultiScale(thisface,1.1,30,1)
			noses=nosefinder.detectMultiScale(thisface,1.1,5,1)
			if len(noses)>0:
				maxnosesize=max([w for (x,y,h,w) in noses])
				biggestnose=[[x,y,h,w] for (x,y,h,w) in noses if w==maxnosesize][0]
				finaleyes=[]
				print "filtering out nostrils from the eyes..."
				for eye in eyes:
					if not (eye[0]>(biggestnose[0]-5) and eye[0]<(biggestnose[0]+biggestnose[3]+5) and eye[1]>(biggestnose[1]-5) and eye[1]<(biggestnose[1]+biggestnose[2]+5)):
						finaleyes.append(eye)
				print "eyes: "+str(finaleyes)
				print "noses: "+str(noses)
				for (x,y,h,w) in finaleyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				for (x,y,h,w) in noses:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(255,255,0),1)
				cv2.imshow("thisface",thisface)
			elif len(eyes)>0:
				print "could not find a nose. working with eyes only"
				for (x,y,h,w) in eyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				cv2.imshow("thisface",thisface)
			else:
				print "could not find any features"