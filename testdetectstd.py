import cv2,time
from scipy import stats

print "defining stuff"
def calibcam(n,cam):
	sumlist=[None]*n
	for i in range(n):
		retval,img=cam.read()
		sumlist[i]=img[240:720,320:960,:].sum()
	return sumlist
def detectchange(threshold,n):
	cam=cv2.VideoCapture(0)
	facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	sumlist=calibcam(n,cam)
	std=stats.tstd(sumlist)
	avg=sum(sumlist)/n
	i=0
	framenum=0
	print "starting detection"
	while True:
		retval,img=cam.read()
		thisz=(img[240:720,320:960,:].sum()-avg)/std
		if abs(thisz)>threshold:
			print "something weird, zscore="+str(thisz)
			time.sleep(1)
			retval,newimg=cam.read()
			#sumlist=calibcam(n,cam)
			#avg=sum(sumlist)/n
			#std=stats.tstd(sumlist)
			faces=facedetector.detectMultiScale(newimg)
			if len(faces)>0:
				print "FOUND A FACEZ!!!!!11!"
				for (x,y,h,w) in faces:
					cv2.rectangle(newimg,(x,y),(x+w,y+h),(0,255,255),1)
				#cv2.imshow("obj num "+str(i),newimg)
				cv2.imshow("obj found",newimg)
			else:
				print "no facez :("
				cv2.imshow("obj not found",newimg)
			i=i+1
			cv2.waitKey(1)
			sumlist[0]=img[240:720,320:960,:].sum()
			std=stats.tstd(sumlist)
			avg=sum(sumlist)/n
		framenum=framenum+1
		if framenum%10==0:
			sumlist[0]=img[240:720,320:960,:].sum()
			std=stats.tstd(sumlist)
			avg=sum(sumlist)/n
		if framenum%100==0:
			print framenum
		#time.sleep(.5)