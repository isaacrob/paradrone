import cv2, sys, os, time, math

imgname=raw_input("image: ")
#imgname="/Users/isaac/Code/jimi.jpg"
img=cv2.imread("/Users/isaac/Code/"+imgname)
img2=cv2.imread("/Users/isaac/Code/"+imgname)
try:
	sp=img.shape
except:
	sys.exit("could not open image ")
print sp

numbranches=int(raw_input("branches: "))

haarface=cv2.CascadeClassifier("/Users/isaac/Code/cvmodcascades/splithaarcascade/facecascade.xml")
lbpface=cv2.CascadeClassifier("/Users/isaac/Code/cvmodcascades/splitlbpcascade/lbpface.xml")
parafaceslbp=[]
parafaceshaar=[]
haartimes=[None]*numbranches
lbptimes=[None]*numbranches
inc=[None]*2
power=1.0/numbranches
inc[0]=int(sp[0]**(power))
inc[1]=int(sp[1]**(power))
scale=min([inc[0]**(1.0/5.0),inc[1]**(1.0/5.0)])
while scale==1.0:
	print("too many branches, scale is 1.0 ")
	numbranches=int(raw_input("branches: "))
	haartimes=[None]*numbranches
	lbptimes=[None]*numbranches
	inc=[None]*2
	power=1.0/numbranches
	inc[0]=int(sp[0]**(power))
	inc[1]=int(sp[1]**(power))
	scale=min([inc[0]**(1.0/5.0),inc[1]**(1.0/5.0)])
print scale
#use either linear or logarithmic spacing

#scale=1.1
actualhaartime=time.time()
actualhaar=haarface.detectMultiScale(img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING))
actualhaartime=time.time()-actualhaartime
actuallbptime=time.time()
actuallbp=lbpface.detectMultiScale(img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING))
actuallbptime=time.time()-actuallbptime

#find para haar
for i in range(numbranches):
	thismin=tuple([min(inc[0]**(i+1),inc[1]**(i+1))]*2)
	thismax=tuple([min(inc[0]**(i+2),inc[1]**(i+2))]*2)
	#try:
	#	scale=((i+1.0)/i)**(1.0/5.0)
	#except:
	#	scale=(float(thismax[0])/thismin[0])**(1.0/5.0)
	#scale=(thismax[0]/thismin[0])**(1.5/(numbranches-i))
	#print scale
	if i==numbranches-1:
		thismax=sp[0:2]
	haartimes[i]=time.time()
	intermid=haarface.detectMultiScale(img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),thismin,thismax)
	haartimes[i]=time.time()-haartimes[i]
	if len(intermid)!=0:
		for rect in intermid:
			parafaceshaar.append(rect)
		cv2.rectangle(img2,(0,0),thismax,(0,255,255),int(round(haartimes[i]*20)))
	else:
		if haartimes[i]>actualhaartime/numbranches:
			cv2.rectangle(img2,(0,0),thismax,(0,0,255),int(round(haartimes[i]*20)))
		else:
			cv2.rectangle(img2,(0,0),thismax,(0,0,0),int(round(haartimes[i]*20)))

#find para lbp
for i in range(numbranches):
	thismin=tuple([min(inc[0]**(i+1),inc[1]**(i+1))]*2)
	thismax=tuple([min(inc[0]**(i+2),inc[1]**(i+2))]*2)
	#scale=(thismax[0]/thismin[0])**(1.0/(numbranches-i))
	#print scale
	#try:
	#	scale=((i+1.0)/i)**(1.0/3.0)
	#except:
	#	scale=(float(thismax[0])/thismin[0])**(1.0/3.0)
	if i==numbranches-1:
		thismax=sp[0:2]
	lbptimes[i]=time.time()
	intermid=lbpface.detectMultiScale(img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),thismin,thismax)
	lbptimes[i]=time.time()-lbptimes[i]
	if len(intermid)!=0:
		for rect in intermid:
			parafaceslbp.append(rect)

#draw para haar
print parafaceshaar
print str((haartimes))+" vs "+str(actualhaartime/numbranches)
for (x,y,h,w) in parafaceshaar:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
print "yellow is haar para face"

#draw para lbp
print parafaceslbp
print str((lbptimes))+" vs "+str(actuallbptime/numbranches)
for (x,y,h,w) in parafaceslbp:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
print "green is lbp para face"

#draw actual haar
print actualhaar
print str(sum(haartimes))+" vs "+str(actualhaartime)+" vs "+str(max(haartimes))
for (x,y,h,w) in actualhaar:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),1)
print "purple is actual haar face"

#draw actual lbp
print actuallbp
print str(sum(lbptimes))+" vs "+str(actuallbptime)+" vs "+str(max(lbptimes))
for (x,y,h,w) in actuallbp:
	cv2.rectangle(img,(x,y,),(x+w,y+h),(0,0,255),1)
print "red is actual lbp face"

cv2.imshow("img",img)
cv2.imshow("time spent",img2)

time.sleep(10000)