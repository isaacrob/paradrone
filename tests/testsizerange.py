def testsizerange(imgname,numstages=10):
	import cv2, sys, time

	img=cv2.imread("/Users/isaac/Code/"+imgname)#raw_input("image? "))
	#numstages=10
	haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	try:
		sp=img.shape
		print sp
	except:
		sys.exit("could not read image")
	power=1.0/(numstages-1)
	bottom=min(sp[0]**(power),sp[1]**(power))
	print bottom
	trans=[None]*numstages
	times=[None]*(numstages-1)
	faces=[]
	trans[0]=(2,2)
	for i in range(1,numstages):
		trans[i]=tuple([int(bottom**(i))]*2)
	print trans
	for i in range(1,numstages):
		starttime=time.time()
		print "running "+str(trans[0])+" to "+str(trans[i])
		inter=haarface.detectMultiScale(img,1.1,3,1,trans[0],trans[i])
		times[i-1]=time.time()-starttime
		print times[i-1]
		print len(inter)
		if len(inter)>0:
			for face in inter:
				faces.append(face)
	for (x,y,h,w) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
	print times
	#figure(1)
	return times
	#cv2.imshow('img',img)
	time.sleep(10000)
def testsizeincexp(imgname,numstages=10):
	import cv2, sys, time

	img=cv2.imread("/Users/isaac/Code/"+imgname)#raw_input("image? "))
	#numstages=10
	haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	try:
		sp=img.shape
		print sp
	except:
		sys.exit("could not read image")
	power=1.0/(numstages-1)
	bottom=min(sp[0]**(power),sp[1]**(power))
	print bottom
	trans=[None]*numstages
	times=[None]*(numstages-1)
	faces=[]
	trans[0]=(2,2)
	for i in range(1,numstages):
		trans[i]=tuple([int(bottom**(i))]*2)
	print trans
	for i in range(1,numstages):
		starttime=time.time()
		print "running "+str(trans[i-1])+" to "+str(trans[i])
		inter=haarface.detectMultiScale(img,1.1,3,1,trans[i-1],trans[i])
		times[i-1]=time.time()-starttime
		print times[i-1]
		print len(inter)
		if len(inter)>0:
			for face in inter:
				faces.append(face)
	for (x,y,h,w) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
	print times
	#figure(1)
	return times
	#cv2.imshow('img',img)
	time.sleep(10000)
def testsizeinclin(imgname,numstages=10):
	import cv2, sys, time

	img=cv2.imread("/Users/isaac/Code/"+imgname)#raw_input("image? "))
	#numstages=10
	haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	try:
		sp=img.shape
		print sp
	except:
		sys.exit("could not read image")
	power=1.0/(numstages-1)
	bottom=min(sp[0]*(power),sp[1]*(power))
	print bottom
	trans=[None]*numstages
	times=[None]*(numstages-1)
	faces=[]
	trans[0]=(2,2)
	for i in range(1,numstages):
		trans[i]=tuple([int(bottom*(i))]*2)
	print trans
	for i in range(1,numstages):
		starttime=time.time()
		print "running "+str(trans[i-1])+" to "+str(trans[i])
		inter=haarface.detectMultiScale(img,1.1,3,1,trans[i-1],trans[i])
		times[i-1]=time.time()-starttime
		print times[i-1]
		print len(inter)
		if len(inter)>0:
			for face in inter:
				faces.append(face)
	for (x,y,h,w) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
	print times
	#figure(1)
	return times
	#cv2.imshow('img',img)
	time.sleep(10000)
def testsizeincparab(imgname,numstages=10):
	import cv2, sys, time

	img=cv2.imread("/Users/isaac/Code/"+imgname)#raw_input("image? "))
	#numstages=10
	haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	try:
		sp=img.shape
		print sp
		sp=min(sp[:1])
	except:
		sys.exit("could not read image")
	def getdist(mynum,total,size,raiseme=2,setmin=10):
		inc=size/((total/2)**raiseme)
		return int(inc*((mynum-total/2))**raiseme+10)/(raiseme+1)
	trans=[None]*numstages
	times=[None]*(numstages-1)
	faces=[]
	trans[0]=(2,2)
	for i in range(1,numstages):
		trans[i]=tuple([trans[i-1][0]+getdist(i,numstages,sp)]*2)
	print trans
	for i in range(1,numstages):
		starttime=time.time()
		print "running "+str(trans[i-1])+" to "+str(trans[i])
		inter=haarface.detectMultiScale(img,1.1,3,1,trans[i-1],trans[i])
		times[i-1]=time.time()-starttime
		print times[i-1]
		print len(inter)
		if len(inter)>0:
			for face in inter:
				faces.append(face)
	for (x,y,h,w) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
	print times
	#figure(1)
	return times
	#cv2.imshow('img',img)
	time.sleep(10000)