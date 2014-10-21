import cv2,time

img=cv2.imread("/Users/isaac/Code/group4.jpg")
facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
scaletime=time.time()
scalefaces=[]
key=set()
interface=facedetector.detectMultiScale(img,1.5,2,1,(67,67),(102,102))
if len(interface)>0:
	for face in interface:
		scalefaces.append(face)
		key.add(face[3])
scaletime=time.time()-scaletime
print scaletime
print len(scalefaces)
print key
indtime=time.time()
indfaces=set()
key=set()
interface=facedetector.detectMultiScale(img,1.5,2,1,(67,67),(68,68))
if len(interface)>0:
	for face in interface:
		indfaces.add(tuple(face))
		key.add(face[3])
print time.time()-indtime
print len(indfaces)
interface=facedetector.detectMultiScale(img,1.5,2,1,(101,101),(102,102))
if len(interface)>0:
	for face in interface:
		indfaces.add(tuple(face))
		key.add(face[3])
print time.time()-indtime
print len(indfaces)
interface=facedetector.detectMultiScale(img,1.5,2,1,(113,113),(114,114))
if len(interface)>0:
	for face in interface:
		indfaces.add(tuple(face))
		key.add(face[3])
indtime=time.time()-indtime
print indtime
print len(indfaces)
print key
for (x,y,h,w) in scalefaces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
for (x,y,h,w) in indfaces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
cv2.imshow("img",img)
time.sleep(1000)