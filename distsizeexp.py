import cv2, time, cPickle, sys
from math import log
import gentimedist as gen

if sys.platform=='darwin':
	file=open("/Users/isaac/Code/parastuff/timedistinfo","r")
	if raw_input("capture img? ")=='n':
		img=cv2.imread("/Users/isaac/Code/group4.jpg")
	else:
		cam=cv2.VideoCapture(0)
		retval,img=cam.read()
	facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
elif sys.platform=='linux2':
	file=open("/home/pi/timedistinfo","r")
	if raw_input("capture img? ")=='n':
		img=cv2.imread("/home/pi/group4.jpg")
	else:
		cam=cv2.VideoCapture(0)
		retval,img=cam.read()
	facedetector=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")
exptimes=cPickle.load(file)
scale=1.1
numnodes=6

sp=min(img.shape[:1])
numsizes=int(log(sp/20)/log(scale))
trans=[None]*numsizes
for i in range(numsizes):
	trans[i]=int(20*(scale**i))

times=gen.loadtimes()
thismin=min(times)
for i in range(numsizes-1):
	times[i]=times[i]-thismin

timepernode=sum(times)/numnodes
print timepernode
thresholds=[None]*(numnodes+1)
thresholds[0]=0

print "predicting even distribution..."
for i in range(1,numnodes+1):
	j=thresholds[i-1]+1
	while sum(times[thresholds[i-1]:j])<timepernode and j<numsizes:
		j=j+1
		#print j
		#time.sleep(3)
	if sum(times[thresholds[i-1]:j])-timepernode>timepernode-sum(times[thresholds[i-1]:j-1]):
		j=j-1 #makes more even, but last few take longest...otherwise even but last is really short
	print sum(times[thresholds[i-1]:j])
	thresholds[i]=j
thresholds[numnodes]=numsizes-1
print thresholds

faces=set()
thistimes=[None]*numnodes
for i in range(numnodes):
	thistimes[i]=time.time()
	thisfaces=facedetector.detectMultiScale(img,scale**2,4,1,tuple([trans[thresholds[i]]-1]*2),tuple([trans[thresholds[i+1]]+1]*2))
	print len(thisfaces)
	if len(thisfaces)>0:
		for face in thisfaces:
			faces.add(tuple(face))
	thistimes[i]=time.time()-thistimes[i]
print thistimes

duptime=time.time()
facelist=list(faces)
donttest=[]
finallist=[]
testlen=len(facelist)
origlist=facelist
testlennew=0
print len(origlist)
while not testlennew==testlen:
	testlen=len(facelist)
	for first in range(len(facelist)):
		if first not in donttest:
			for second in range(first+1,len(facelist)):
				sub=facelist[first]
				j=facelist[second]
				var=abs(j[3]-sub[3])/2
				if ((j[0]+j[3]/2-var<sub[0]+sub[3]/2) and (j[0]+j[3]/2+var>sub[0]+sub[3]/2)) and ((j[1]+j[2]/2-var<sub[1]+sub[2]/2) and (j[1]+j[2]/2+var>sub[1]+sub[2]/2)) and min([float(j[3])/sub[3],float(sub[3])/j[3]])>1.0/2.0:
					donttest.append(first)
					donttest.append(second)
					#facelist.append(tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2]))
					inter=tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2])
					finallist.append(inter)
					break
			if first not in donttest:
				finallist.append(facelist[first])
	testlennew=len(finallist)
	facelist=finallist
	finallist=[]
	donttest=[]
finallist=facelist
duptime=time.time()-duptime
print len(finallist)

serialtime=time.time()
facedetector.detectMultiScale(img,scale,4,1)
serialtime=time.time()-serialtime
print serialtime

for (x,y,h,w) in finallist:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
cv2.imshow("img",img)
time.sleep(30)