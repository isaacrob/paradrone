def findfaces(imgname,profile='default',raiseme=1):
	import cv2, sys, time, math, operator
	from IPython.parallel import *
	
	#this will push the image and have all the processing on the pis (for now)
	#just for haar (for now)
	c=Client(profile=profile)
	dview=c[:]
	dview.block=False
	with dview.sync_imports():
		import cv2, sys, time, math
	img=cv2.imread("/Users/isaac/Code/"+imgname)
	try:
		sp=img.shape
	except:
		sys.exit("could not open image ")

	numbranches=len(c.ids)

	#upload
	starttime=time.time()
	dview["img"]=img
	dview.execute("img=img.copy()",)#block=True)
	starttime=time.time()-starttime
	print "sending out image took "+str(starttime)

	#try:
	for i in c.ids:
		c[i].execute('if sys.platform=="darwin": haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")')
		c[i].execute('if sys.platform=="linux2": haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")')
	plat=sys.platform
	if plat=='darwin':
		haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	elif plat=='linux2':
		haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")
	else:
		sys.exit("did not recognize sys.platform")
	#except:
	#	sys.exit("could not open cascade, perhaps wrong os, in which case FIX IT ")
	

	#dview["haarface"]=haarface
	#can't pickle a haarcascade
	#dview.execute("haarface=cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml')")
	#will only work on mac
	parafaceshaar=[]
	inc=[None]*2
	#raiseme=1.25
	power=(numbranches-1)**raiseme
	inc[0]=int(sp[0]/(power))
	inc[1]=int(sp[1]/(power))
	subframes=10
	print inc

	actualhaartime=time.time()
	actualhaar=haarface.detectMultiScale(img,1.1,subframes,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING))
	actualhaartime=time.time()-actualhaartime

	for i in range(numbranches):
		thismin=int(min(inc[0]*(i**raiseme),inc[1]*(i**raiseme)))
		thismax=int(min(inc[0]*((i+1)**raiseme),inc[1]*((i+1)**raiseme)))
		if thismin==0 or thismin==1:
			thismin=min(15,min(sp[0]/4,sp[1]/4))
			if thismin==1 or thismin==0:
				thismin=2
		scalestart=float(thismax)/thismin
		scale=scalestart**(1.0/subframes)
		j=1
		while scale==1.0:
			scale=scalestart**(1.0/(subframes-j))
			j=j+1
		if scale==0.0:
			scale=1.1
		#if scale>1.1:
		#	scale=1.1
		c[c.ids[i]]["scale"]=scale
		c[c.ids[i]]["subframes"]=(subframes-j)/3
		c[c.ids[i]]["thismin"]=tuple([thismin]*2)
		c[c.ids[i]]["thismax"]=tuple([thismax]*2)
		print str(c.ids[i])+": "+str(thismin)+" thru "+str(thismax)
		if i==numbranches-1:
			c[c.ids[i]]["thismax"]=sp[0:2]

	paratime=time.time()
	print "execution started "+str(paratime)
	#dview.execute("faceshaar=haarface.detectMultiScale(img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),thismin,thismax)",block=True)
	for i in c.ids:
		print str(i)+" started at "+str(time.time())
		c[i].execute("exectime=time.time();faceshaar=haarface.detectMultiScale(img,scale,subframes,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),thismin,thismax);exectime=time.time()-exectime;endtime=time.time()",block=False)
	#for i in c.ids:
	#	parafaceshaar.append(c[i].apply_async(haarface.detectMultiScale,img,scale,numbranches*2,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING),c[i]["thismin"],c[i]["thismax"]))
	#numrm=0
	#for i in len(c.ids):
	#	inter=parafaceshaar[i-numrm].get()
	#	if len(inter)!=0:
	#		parafaceshaar[i-numrm]=inter
	#	else:
	#		parafaceshaar[i-numrm]=[]
	#		numrm=numrm+1
	print "execute took "+str(time.time()-paratime)
	for i in c.ids:
		try:
			inter=c[i]["faceshaar"][:]
			print str(i)+" found: "+str(inter)
			if len(inter)!=0:
				for sub in inter:
			#for sub in inter:
			#	for (x,y,h,w) in parafaceshaar:
			#		if ((x+w/2-5<sub[0]+sub[3]/2) and (x+w/2+5>sub[0]+sub[3]/2)) and ((y+h/2-5<sub[1]+sub[2]/2) and (y+h/2+5>sub[1]+sub[2]/2)):
			#			print "got this far"
			#			print parafaceshaar
			#			parafaceshaar.remove(tuple([x,y,h,w]))
			#			sub=tuple([(x+sub[0])/2,(y+sub[1])/2,(h+sub[2])/2,(w+sub[3])/2])
			#		else:
			#			print "no duplicates with this one: "+str(sub)
					parafaceshaar.append(sub)
		except IndexError as e:
			print "there was a problem retrieving "+str(i)+", "+str(e)
		#except:
		#	print "there was a problem retrieving "+str(i)+", some other problem that should be checked out"
		print str(i)+" retrieved at "+str(time.time())
	paratime=time.time()-paratime
	timelist=[]
	for i in c.ids:
		timelist.append(c[i]["exectime"])
		print str(i)+" ended at "+str(c[i]["endtime"])
	print "time actually spent executing (ind.,total): "+str(timelist)+", "+str(sum(timelist))

	print parafaceshaar
	print "checking for false duplicates..."
	duptime=time.time()
	donttest=[]
	finallist=[]
	testlen=len(parafaceshaar)
	origlist=parafaceshaar
	testlennew=0
	while not testlennew==testlen:
		testlen=len(parafaceshaar)
		for first in range(len(parafaceshaar)):
			if first not in donttest:
				for second in range(first+1,len(parafaceshaar)):
					sub=parafaceshaar[first]
					j=parafaceshaar[second]
					var=abs(j[3]-sub[3])/2
					if ((j[0]+j[3]/2-var<sub[0]+sub[3]/2) and (j[0]+j[3]/2+var>sub[0]+sub[3]/2)) and ((j[1]+j[2]/2-var<sub[1]+sub[2]/2) and (j[1]+j[2]/2+var>sub[1]+sub[2]/2)) and min([float(j[3])/sub[3],float(sub[3])/j[3]])>1.0/2.0:
						donttest.append(first)
						donttest.append(second)
						#parafaceshaar.append(tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2]))
						inter=tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2])
						finallist.append(inter)
						break
				if first not in donttest:
					finallist.append(parafaceshaar[first])
		testlennew=len(finallist)
		parafaceshaar=finallist
		print parafaceshaar
		finallist=[]
		donttest=[]
	finallist=parafaceshaar
	print time.time()-duptime
	print finallist
	#donttest.sort()
	#endpoint=len(donttest)
	#for i in range(endpoint):
	#	parafaceshaar.pop(donttest[endpoint-i-1])

	for (x,y,h,w) in finallist: #changed from parafaceshaar
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
	#for (x,y,h,w) in origlist: #changed from parafaceshaar
	#	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	for (x,y,h,w) in actualhaar:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),1)

	#img=cv2.resize(img,(500,int(500*float(sp[0])/sp[1])))

	print "para: "+str(paratime)+"/"+str(paratime+starttime)+", normal: "+str(actualhaartime)
	for time in timelist:
		print time
		if time>1000000000:
			print "time too large"
			timelist[timelist.index(time)]=0
	return timelist