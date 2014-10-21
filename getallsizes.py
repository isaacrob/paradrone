import cv2
from math import log

img=cv2.imread("/Users/isaac/Code/group4.jpg")
facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
scale=1.12435388628
faces=facedetector.detectMultiScale(img,scale,5,1)
sizes=set()
def logvarbase(x,base):
	return log(x)/log(base)
for face in faces:
	sizes.add(face[3])
sortedsizes=list(sizes)
sortedsizes.sort()
ratios=[None]*(len(sortedsizes)-1)
for i in range(1,len(sortedsizes)):
	ratios[i-1]=[float(sortedsizes[i])/sortedsizes[i-1],logvarbase(float(sortedsizes[i])/20,scale)]
print sortedsizes
print ratios
print len(faces)
print float(min(img.shape[:1]))/max(sortedsizes)
print float(max(img.shape[:1]))/max(sortedsizes)
print img.shape