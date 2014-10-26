import cv2, copy
import numpy as np
facefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
eyefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_eye.xml")
nosefinder=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_mcs_nose.xml")
while not raw_input("find and align face? y/n ")=='n':
	cv2.destroyAllWindows()
	print "finding faces..."
	cam=cv2.VideoCapture(1)
	retval,img=cam.read()
	if not retval:
		print "could not read image"
	cam.release()
	#cv2.imshow("img",img)
	dims=facefinder.detectMultiScale(img,1.1,4,1,(20,20),img.shape[:2])
	print dims
	if len(dims)>0:
		sizelist=[w for (x,y,h,w) in dims]
		maxsize=max(sizelist)
		biggestface=[[x,y,h,w] for (x,y,h,w) in dims if w==maxsize and w>60]
		print biggestface
		if len(biggestface)>0:
			print "finding facial features..."
			for (x,y,h,w) in biggestface:
				thisface=img[x:(x+w),y:(y+h),:]
				cleanface=copy.deepcopy(thisface)
			cv2.imshow("thisface",thisface)
			eyes=eyefinder.detectMultiScale(thisface,1.1,30,1)
			noses=nosefinder.detectMultiScale(thisface,1.1,20,1)
			print "eyes: "+str(eyes)
			print "noses: "+str(noses)
			if len(noses)>0 and len(eyes)>1:
				maxnosesize=max([w for (x,y,h,w) in noses])
				biggestnose=[[x,y,h,w] for (x,y,h,w) in noses if w==maxnosesize][0]
				finaleyes=[]
				print "filtering out nostrils from the eyes..."
				for eye in eyes:
					if not (eye[0]>(biggestnose[0]-5) and eye[0]<(biggestnose[0]+biggestnose[3]+5) and eye[1]>(biggestnose[1]-5) and eye[1]<(biggestnose[1]+biggestnose[2]+5)):
						finaleyes.append(eye)
				print "eyes: "+str(finaleyes)
				print "noses: "+str(noses)
				for (x,y,h,w) in finaleyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				for (x,y,h,w) in [biggestnose]:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(255,255,0),1)
				#print biggestnose
				cv2.imshow("thisface features",thisface)
				eye1mid=(finaleyes[0][0]+finaleyes[0][3]/2,finaleyes[0][1]+finaleyes[0][2]/2)
				try:
					eye2mid=(finaleyes[1][0]+finaleyes[1][3]/2,finaleyes[1][1]+finaleyes[1][2]/2)
				except:
					print "something went wrong with the format of eyes, skipping to next iteration"
					continue
				if eye1mid[0]<eye2mid[0]:
					lefteye=eye1mid
					righteye=eye2mid
				else:
					lefteye=eye2mid
					righteye=eye1mid
				borderoffset=9.0/12.0
				midborderoffset=3
				eyetriangle=[righteye[0]-lefteye[0],righteye[1]-lefteye[1]]
				topbordermid=[lefteye[0]+eyetriangle[0]/2+eyetriangle[1]/midborderoffset,lefteye[1]+eyetriangle[1]/2-eyetriangle[0]/midborderoffset]
				topborder=[(topbordermid[0]-int(eyetriangle[0]*borderoffset),topbordermid[1]-int(eyetriangle[1]*borderoffset)),(topbordermid[0]+int(eyetriangle[0]*borderoffset),topbordermid[1]+int(eyetriangle[1]*borderoffset))]
				bordertriangle=[topborder[1][0]-topborder[0][0],topborder[1][1]-topborder[0][1]]
				borderlength=int(np.sqrt(bordertriangle[0]**2+bordertriangle[1]**2))
				print bordertriangle
				border=[topborder[0],topborder[1],(topborder[1][0]-bordertriangle[1],topborder[1][1]+bordertriangle[0]),(topborder[0][0]-bordertriangle[1],topborder[0][1]+bordertriangle[0])]
				violation=0
				for i in range(4):
					for j in range(2):
						if border[i][j]>thisface.shape[0] or border[i][j]<0:
							violation=1			
				if violation:
					print "could not align face, features too close to edge"
				else:
					print "aligning face"
					cv2.line(thisface,eye1mid,eye2mid,(255,0,0),1)
					cv2.line(thisface,border[0],border[1],(0,255,0),1)
					cv2.line(thisface,border[2],border[3],(0,255,0),1)
					cv2.line(thisface,border[0],border[3],(0,255,0),1)
					cv2.line(thisface,border[1],border[2],(0,255,0),1)
					#cv2.line(thisface,(nosemid[0]+eyedist,nosemid[1]+noseedgeoffset),(nosemid[0]-eyedist,nosemid[1]+noseedgeoffset),(0,255,0),1)
					facecenter=tuple(np.array([border[0][0]+border[2][0],border[0][1]+border[2][1]])/2)
					cv2.circle(thisface,facecenter,5,(255,0,0),-1)
					cv2.imshow("thisface border",thisface)
					rotationangle=np.arctan(float(eyetriangle[1])/float(eyetriangle[0]))
					rotationmat=cv2.getRotationMatrix2D(facecenter,rotationangle*180/np.pi,1.0)
					print border[0]
					bordercenteroffset=[border[0][0]-facecenter[0],border[0][1]-facecenter[1]]
					print bordercenteroffset
					borderoffsetafterrotation=[bordercenteroffset[0]*np.cos(rotationangle)+bordercenteroffset[1]*np.sin(rotationangle),bordercenteroffset[0]*np.sin(rotationangle)-bordercenteroffset[1]*np.cos(rotationangle)-borderlength]
					print borderoffsetafterrotation
					borderafterrotation=(int(borderoffsetafterrotation[0]+facecenter[0]),int(borderoffsetafterrotation[1]+facecenter[1]))
					print borderafterrotation
					finalface=cv2.warpAffine(thisface,rotationmat,thisface.shape[:2],flags=cv2.INTER_LINEAR)
					finalcroppedface=finalface[borderafterrotation[1]:borderlength+borderafterrotation[1],borderafterrotation[0]:borderafterrotation[0]+borderlength]
					cv2.circle(finalface,borderafterrotation,3,(0,255,0),-1)
					#cv2.circle(finalface,(borderafterrotation[0],borderafterrotation[1]-borderlength),3,(0,255,0),-1)
					cv2.circle(finalface,facecenter,4,(0,255,255),-1)
					cv2.imshow("rotated",finalface)
					cv2.imshow("final cropped face",finalcroppedface)
					cleanface=cv2.warpAffine(cleanface,rotationmat,thisface.shape[:2],flags=cv2.INTER_LINEAR)[borderafterrotation[1]:borderlength+borderafterrotation[1],borderafterrotation[0]:borderafterrotation[0]+borderlength]
					cv2.imshow("clean face",cleanface)
			elif len(eyes)>1:
				print "could not find a nose. working with eyes only"
				for (x,y,h,w) in eyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				cv2.imshow("thisface",thisface)
			else:
				print "could not find enough features"