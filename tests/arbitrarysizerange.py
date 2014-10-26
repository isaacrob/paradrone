import cv2,sys,time

img=cv2.imread("/Users/isaac/Code/group4.jpg")
facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
threshlist=[20,150,285,420,555,690,825,960,1095,1230,1365]
indsubwincounts=[0]*10
#for i in range(11):
#	threshlist[i]=threshlist[i]/2
#threshlist[0]=2
scalelist=[1.0]*10
timelist=[0]*10
averagetimes=[0]*10
facelist=[]
subwincount=11
while 1.0 in scalelist:
	subwincount=subwincount-1
	for i in range(10):
		scalelist[i]=(float(threshlist[i+1])/threshlist[i])**(1.0/subwincount)
print "subwindows: "+str(subwincount)
for i in range(10):
	for j in range(subwincount):
		indsubwincounts[i]=indsubwincounts[i]+int((1365-threshlist[i]*(scalelist[i]**j)+1)**2)
print indsubwincounts
for i in range(11):
	threshlist[i]=tuple([threshlist[i]]*2)
for i in range(10):
	#print "from "+str(threshlist[i])+" to "+str(threshlist[i+1])+", at a scale of "+str(scalelist[i])
	timelist[i]=time.time()
	interface=facedetector.detectMultiScale(img,scalelist[i],subwincount,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),threshlist[i],threshlist[i+1])
	if len(interface)>0:
		for face in interface:
			facelist.append(face)
	timelist[i]=time.time()-timelist[i]
print "faces found: "+str(len(facelist))
print "time taken: "+str(timelist)
for i in range(10):
	averagetimes[i]=timelist[i]/indsubwincounts[i]
print "average times per subwindow: "+str(averagetimes)