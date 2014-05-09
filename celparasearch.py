from celparaworker import *
import numpy
from subprocess import *
from math import *
import time
numworkers=int(raw_input('How many workers? '))
networkingspeed=float(raw_input('Networking speed? '))
size=int(raw_input('How large of an area? '))
algorithm=raw_input('Which algorithm? ')
def genmyspotlist(myspot):
	myspotlist=[None]*8
	myspotlist[0]=(myspot[0]-1,myspot[1]-1)
	myspotlist[1]=(myspot[0],myspot[1]-1)
	myspotlist[2]=(myspot[0]+1,myspot[1]-1)
	myspotlist[3]=(myspot[0]-1,myspot[1])
	myspotlist[4]=(myspot[0]+1,myspot[1])
	myspotlist[5]=(myspot[0]-1,myspot[1]+1)
	myspotlist[6]=(myspot[0],myspot[1]+1)
	myspotlist[7]=(myspot[0]+1,myspot[1]+1)
	return myspotlist
background=numpy.zeros((size,size))
for i in range(0,numworkers):
	#Popen(['/Users/isaac/Code/celparaworker.py'])
	print 'initialized worker '+str(i+1)
spots=[None]*numworkers
oldspots=[]
for i in range(0,numworkers):
	intermidspot=(int(numpy.random.rand()*size),\
	            int(numpy.random.rand()*size))
	while intermidspot in spots:
		intermidspot=(int(numpy.random.rand()*size),\
		        int(numpy.random.rand()*size))
	spots[i]=intermidspot
	print 'worker at '+str(intermidspot)
	background[intermidspot[0],intermidspot[1]]=1
print 'starting the search'
print background
iteration=1
oldspots.append(tuple(spots))
centerspot=spots[0]
centerspots=genmyspotlist(centerspot)
alert=None
while 0 in background:
	print 'iteration '+str(iteration)+', from '\
	                +str(oldspots[iteration-1])
	if algorithm=='nextlocation':
		for i in range(0,numworkers):
			spots[i]=nextlocation.delay(background,networkingspeed,\
			             spots[i])
		for i in range(0,numworkers):
			intermidspot=spots[i].get()
			spots[i]=intermidspot
			background[intermidspot[0],intermidspot[1]]\
			       =background[intermidspot[0],\
			       intermidspot[1]]+1
		intermidspot=None
	if algorithm=='repel':
		repelget=[None]*numworkers
		distances=[None]*numworkers
		proposedpoints=[None]*numworkers
		for i in range(0,numworkers):
			repelget[i]=repel.delay(spots,centerspots[i],background)
		for i in range(0,numworkers):
			intermiddata=repelget[i].get()
			distances[i],proposedspots[i]=intermiddata
		spots=proposedspots[max[distances]]
		for i in spots:
			background[i[0],i[1]]=background[i[0],i[1]]+1
		centerspot=spots[0]
		centerspots=genmyspotlist(centerspot)
	if algorithm=='gotoedge':
		center=[None,None]
		center[0]=sum([x for x,y in spots])/len(spots)
		center[1]=sum([y for x,y in spots])/len(spots)
		starttime=time.time()
		for i in range(0,numworkers):
			spots[i]=gotoedge.delay(center,spots[i],background)
		for i in range(0,numworkers):
			intermidspot=spots[i].get()
			if intermidspot in spots[0:(len(spots)-1)]:
				alert='problem with drones wanting to move to '\
				        +str(intermidspot)\
				        +' from '+str(oldspots[iteration-1][i])
				spots[i]=[None]
				spots[i]=gotoedge.delay(center,oldspots[iteration-1][i],\
				            background,\
				            nope=intermidspot)
				intermidspot=spots[i].get()
			spots[i]=intermidspot
			background[intermidspot[0],intermidspot[1]]\
			             =background[intermidspot[0],\
			             intermidspot[1]]+1
		intermidspot=None
	print 'new points: '+str(spots)
	print background
	x,y=numpy.where(background>0)
	zerospots=zip(x,y)
	print 'percent done: '+str((float(len(zerospots))/(size**2))*100)+'%'
	print 'time taken this iteration: '+str(time.time()-starttime)
	print alert
	alert=None
	oldspots.append(tuple(spots))
	iteration=iteration+1
print 'final report: '
print 'moves wasted: '+str(-size**2+numworkers*iteration-(size**2)\
                %numworkers)
print 'workers: '+str(numworkers)
print 'number of squares: '+str(size**2)
print 'extra iterations: '+str(iteration-ceil(size**2/numworkers))
print 'percent error in terms of iterations: '+str((iteration-\
                ceil(size**2/numworkers\
                ))/iteration*100)+'%'