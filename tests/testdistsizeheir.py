import cv2,sys,time,random

#works nearly perfectly with totalframes=50 numnodes=6 absmin=40
#totalframes=100
numnodes=30
totalframes=int(min(8*numnodes,numnodes**(.5)*30))
print totalframes
pernode=totalframes/numnodes
img=cv2.imread("/Users/isaac/Code/jimi.jpg")
facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
sp=min(img.shape[:1])
print sp
absmin=75 #int(min(40,500/numnodes))
scale=(sp/absmin)**(1.0/(pernode+1))
print scale
mins=[None]*numnodes
inc=scale*absmin/numnodes
mins[0]=absmin-numnodes*inc/2 #absmin
timelist=[0]*numnodes
facelist=set()
nodefacelist=[]
for i in range(1,numnodes):
	mins[i]=mins[i-1]+inc
for i in range(numnodes):
	mins[i]=tuple([int(mins[i])]*2)
print mins
for i in range(numnodes):
	timelist[i]=time.time()
	interface=facedetector.detectMultiScale(img,scale,2,1,mins[i])
	if len(interface)>0:
		nodefacelist.append(interface)
		print str(i)+" found "+str(len(interface))+" faces"
		for face in interface:
			facelist.add(tuple(face.tolist()))
	timelist[i]=time.time()-timelist[i]
duptime=time.time()
facelist=list(facelist)
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
print duptime
print len(finallist)
print timelist
print sum(timelist)
serialtime=time.time()
faces=facedetector.detectMultiScale(img)
serialtime=time.time()-serialtime
print serialtime
print "("+str(serialtime/numnodes)+" v "+str(max(timelist))+" v "+str(sum(timelist)/numnodes)+")"
print len(faces)
for (x,y,h,w) in finallist:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
for i in range(len(nodefacelist)):
	color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
	if i==0:
		thickness=2
	else:
		thickness=1
	for (x,y,h,w) in nodefacelist[i]:
		cv2.rectangle(img,(x,y),(x+w,y+h),color,thickness)
cv2.imshow("img",img)
time.sleep(10000)