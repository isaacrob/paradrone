import cv2
import numpy as np
imgset=[]
labels=[]
facefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
while raw_input("capture img? y/n ")=='y':
	cam=cv2.VideoCapture(1)
	retval,img=cam.read()
	cam.release()
	dims=facefinder.detectMultiScale(img,1.1,4,(1),(20,20),img.shape[:2])
	#dims=dims[0]
	print dims
	if len(dims)>0:
		sizelist=[w for (x,y,h,w) in dims]
		maxsize=max(sizelist)
		biggestface=[[x,y,h,w] for (x,y,h,w) in dims if w==maxsize and w>60]
		print biggestface
	#for i in range(len(dims)):
	#	thisface=img[dims[i][0]:(dims[i][0]+dims[i][3]),dims[i][1]:(dims[i][1]+dims[i][2]),:]
	#	thisface=cv2.cvtColor(thisface,cv2.COLOR_BGR2GRAY)
	#	try:
	#		thisface=cv2.resize(thisface,(60,60))
	#	except:
	#		pass
	#	print thisface.shape
	#	cv2.imshow("thisface",thisface)
	#	if raw_input("is this the correct face? y/n ")=='y':
	#		imgset.append(thisface)
	#		break
		if biggestface:
			for (x,y,h,w) in biggestface:
				thisface=img[x:(x+w),y:(y+h),:]
				thisface=cv2.cvtColor(thisface,cv2.COLOR_BGR2GRAY)
				thisface=cv2.resize(thisface,(60,60))
				cv2.imshow("thisface",thisface)
				if raw_input("is this the correct face? y/n ")=='y':
					imgset.append(thisface)
					labels.append(int(raw_input("who is this? (int) ")))
	#labels.append(int(raw_input("who is this? (int) ")))
labels=np.array(labels)
facerec=cv2.createLBPHFaceRecognizer()
facerec.train(imgset,labels)
while raw_input("predict again? y/n ")=='y':
	cam=cv2.VideoCapture(1)
	retval,img=cam.read()
	cam.release()
	dims=facefinder.detectMultiScale(img,1.1,4,(1),(20,20),img.shape[:2])
	#dims=dims[0]
	print dims
	if len(dims)>0:
		sizelist=[w for (x,y,h,w) in dims]
		maxsize=max(sizelist)
		biggestface=[[x,y,h,w] for (x,y,h,w) in dims if w==maxsize and w>60]
		print biggestface
	#for (x,y,h,w) in dims:
	#	thisface=img[x:(x+w),y:(y+h),:]
	#	thisface=cv2.cvtColor(thisface,cv2.COLOR_BGR2GRAY)
	#	try:
	#		thisface=cv2.resize(thisface,(60,60))
	#	except:
	#		pass
	#	print thisface.shape
	#	cv2.imshow("thisface",thisface)
	#	if raw_input("is this the correct face? y/n ")=='y':
	#		break
		if biggestface:
			for (x,y,h,w) in biggestface:
				thisface=img[x:(x+w),y:(y+h),:]
				thisface=cv2.cvtColor(thisface,cv2.COLOR_BGR2GRAY)
				thisface=cv2.resize(thisface,(60,60))
				cv2.imshow("checkedface",thisface)
				if raw_input("is this the correct face? y/n ")=='y':
					print facerec.predict(thisface)
	