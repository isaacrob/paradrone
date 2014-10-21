import cv2, sys, os, time, math

scale=6

imgname=raw_input("image: ")
#imgname="/Users/isaac/Code/jimi.jpg"
img=cv2.imread("/Users/isaac/Code/"+imgname)
try:
	sp=img.shape
except:
	sys.exit("could not open image ")

#dir=raw_input("location of lbp split cascade directory: ")
dir="/Users/isaac/Code/cvmodcascades/splitlbpcascade"
dir2="/Users/isaac/Code/cvmodcascades/splithaarcascade"
def runsplitcascade(dir):
	try:
		(a,b,cascadepieces)=os.walk(dir).next()
	except:
		sys.exit("could not work with specified directory ")

	print "assuming all files except last 2 are pieces of the cascade "
	numpieces=len(cascadepieces)-2
	piecehandler=[None]*numpieces
	for i in range(numpieces):
		try:
			piecehandler[i]=cv2.CascadeClassifier(dir+"/"+cascadepieces[i])
		except:
			print "something went wrong retrieving "+cascadepieces[i]+", continuing without it"

	resultlist=[None]*numpieces
	mixedresults=[]
	#numerrors=0
	for i in range(numpieces):
		print i
		try:
			for rect in piecehandler[i].detectMultiScale(img,1.3,10,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),(sp[0]/scale,sp[1]/scale)):
				mixedresults.append(rect)
			#resultlist[i-numerrors]=piecehandler[i].detectMultiScale(img,5,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),(60,60))
		except:
			print "something went wrong using "+cascadepieces[i]+", continuing without it "
			#numerrors=numerrors+1
		#for rect in resultlist[i-numerrors]:
		#	mixedresults.append(rect)
	return mixedresults

mixedresultslbp=runsplitcascade(dir)
mixedresultshaar=runsplitcascade(dir2)

fullcascade=cv2.CascadeClassifier("/Users/isaac/Code/cvmodcascades/splitlbpcascade/lbpface.xml")
realspot=fullcascade.detectMultiScale(img,1.1,5,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),(sp[0]/scale,sp[1]/scale))
fullcascadehaar=cv2.CascadeClassifier("/Users/isaac/Code/cvmodcascades/splithaarcascade/facecascade.xml")
realspothaar=fullcascadehaar.detectMultiScale(img,1.1,5,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),(sp[0]/scale,sp[1]/scale))

sumlbp=[0,0]
sumhaar=[0,0]

for (x,y,h,w) in mixedresultslbp:
	sumlbp[0]=sumlbp[0]+x
	sumlbp[1]=sumlbp[1]+y
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),1)
print "white is lbp individual cascades"
for (x,y,h,w) in mixedresultshaar:
	sumhaar[0]=sumhaar[0]+x
	sumhaar[1]=sumhaar[1]+y
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
print "yellow is haar individual cascades"

sumlbp[0]=sumlbp[0]/len(mixedresultslbp)
sumlbp[1]=sumlbp[1]/len(mixedresultslbp)
sumhaar[0]=sumhaar[0]/len(mixedresultshaar)
sumhaar[1]=sumhaar[1]/len(mixedresultshaar)

(locations,weight)=cv2.groupRectangles(mixedresultslbp,5)
for (x,y,h,w) in locations:
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.circle(img,(x,y),10,(0,255,0),2)
	print str(sp[1]/2)+", "+str(sp[0]/2)+" vs "+str(x+w/2)+", "+str(y+h/2)
#locations=tuple([sumlbp[0],sumlbp[1],max(mixedresultslbp[:][2]),max(mixedresultslbp[:][3])])
cv2.circle(img,(sumlbp[0],sumlbp[1]),15,(0,255,0),5)
#cv2.rectangle(img,(locations[0],locations[1]),(locations[0]+locations[2],locations[1]+locations[3]),(0,255,0),2)
print "green is clustered lbp cascades"

i=19
(locations,weight)=cv2.groupRectangles(mixedresultshaar,i)
while len(locations)==0:
	i=i-1
	(locations,weight)=cv2.groupRectangles(mixedresultshaar,i)
#locations=tuple([sumhaar[0],sumhaar[1],max(mixedresultshaar[:][2]),max(mixedresultshaar[:][3])])
for (x,y,h,w) in locations:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	cv2.circle(img,(x,y),10,(255,0,0),2)
	print "(haar) "+str(sp[1]/2)+", "+str(sp[0]/2)+" vs "+str(x+w/2)+", "+str(y+h/2)
cv2.circle(img,(sumhaar[0],sumhaar[1]),15,(255,0,0),5)
#cv2.rectangle(img,(locations[0],locations[1]),(locations[0]+locations[2],locations[1]+locations[3]),(255,0,0),2)
print "blue is clustered haar cascades"
	
for (x,y,h,w) in realspot:
	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
	print "(actual) "+str(sp[1]/2)+", "+str(sp[0]/2)+" vs "+str(x+w/2)+", "+str(y+h/2)
print "red is actual lbp prediction"
for (x,y,h,w) in realspothaar:
	cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
	print "(actual) (haar) "+str(sp[1]/2)+", "+str(sp[0]/2)+" vs "+str(x+w/2)+", "+str(y+h/2)
print "purple is actual haar prediction"
cv2.imshow("img",img)

time.sleep(10000)
#print location