#! /usr/bin/env python
from celery import Celery
import time, numpy
from math import *
app = Celery('celparaworker', backend='amqp', broker='amqp://')
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
def nearestzero(myspot,map):
	myspotlist=genmyspotlist(myspot)
	listofbadspots=[]
	for i in range(0,8):
		if len(map) in myspotlist[i] or -1 in myspotlist[i]:
			listofbadspots.append(myspotlist[i])
	for i in listofbadspots:
		myspotlist.remove(i)
	x,y=numpy.where(map==0)
	zerospots=zip(x,y)
	if len(zerospots)==0:
		print 'could not find any zeros, will stay put'
		return myspot
	zerodists=[None]*len(zerospots)
	for i in range(0,len(zerospots)):
		zerodists[i]=sqrt((myspot[0]-zerospots[i][0])**2+(myspot[1]-\
		       zerospots[i][1])**2)
	closestzero=zerospots[zerodists.index(min(zerodists))]
	distlist=[None]*len(myspotlist)
	for i in range(0,len(myspotlist)):
		distlist[i]=sqrt((closestzero[0]-myspotlist[i][0])**2+\
		         (closestzero[1]-myspotlist[i][1])**2)
	return tuple(myspotlist[distlist.index(min(distlist))])
@app.task
def waitplease(n):
	time.sleep(n)
@app.task
def nextlocation(recievedmap,networkingspeed,myspot):
	x,y=numpy.where(recievedmap>0)
	otherspots=zip(x,y)
	myspotlist=genmyspotlist(myspot)
	listofbadspots=[]
	for i in range(0,8):
		if len(recievedmap) in myspotlist[i] or -1 in myspotlist[i] \
		        or recievedmap[myspotlist[i][0],myspotlist[i][1]]!=0:
			listofbadspots.append(myspotlist[i])
	for i in listofbadspots:
		myspotlist.remove(i)
	distances=[None]*len(myspotlist)
	middistances=[None]*len(otherspots)
	for i in range(0,len(myspotlist)):
		for j in range(0,len(otherspots)):
			middistances[j]=sqrt((myspotlist[i][0]-otherspots[j][0])**2\
			       +(myspotlist[i][1]-otherspots[j][1])**2)
		distances[i]=sum(middistances)
	bestspotindex=distances.index(max(distances))
	bestspot=myspotlist[bestspotindex]
	time.sleep(networkingspeed)
	return bestspot
@app.task
def repel(otherspots,myspot,map):
	#not working yet
	if map[myspot[0],myspot[1]]!=0:
		return []
	otherspotlist=[None]*len(otherspots)
	distlists=[None]*len(otherspots)
	for j in range(0,len(otherspots)):
		otherspotlist[j]=genmyspotlist(otherspots[j])
		listofbadspots=[]
		for i in range(0,8):
			if len(map) in otherspotlist[j][i] \
			        or -1 in otherspotlist[j][i] \
			        or map[otherspotlist[j][i][0],otherspotlist[j]\
			    	[i][1]]!=0:
				listofbadspots.append(otherspotlist[j][i])
		for i in listofbadspots:
			otherspotlist[j].remove(i)
		distlists[j]=[None]*len(otherspotlist[j])
		for i in range(0,len(otherspotlist[j])):
			distlists[j][i]=sqrt((myspot[0]-otherspotlist[j][i][0])**2+\
			        (myspot[1]-otherspotlist[j][i][1])**2)
	addresses=[]
	complist=[None]*len(addresses)
	for a in range(0,len(distlists[0])):
		for b in range(0,len(distlists[1])):
			for c in range(0,len(distlists[2])):
				for d in range(0,len(distlists[3])):
					for e in range(0,len(distlists[4])):
						for f in range(0,len(distlists[5])):
							for g in range(0,len(distlists[6])):
								addresses.append([a,b,c,d,e,f,g])
	for i in range(0,len(addresses)):
		middists=[None]*7
		for j in range(0,7):
			middists[j]=distlists[j][addresses[i][j]]
		addresses[i].append(sum(middists))
		complist[i]=sum(middists)
	finallocation=complist.index(max(complist))
	finalspots=[None]*7
	for i in range(0,addresses[finallocation]):
		finalspots[i]=addresses[finallocation][i]
	return [complist[finallocation],[myspot,finalspots]]
@app.task
def gotoedge(center,myspot,map,nope=False):
	oktogo=0
	repeats=0
	myspotlist=genmyspotlist(myspot)
	if nope:
		myspotlist.remove(nope)
	listofbadspots=[]
	for i in range(0,len(myspotlist)):
		if len(map) in myspotlist[i] or -1 in myspotlist[i] or map[\
		             myspotlist[i][0],myspotlist[i][1]]!=0:
			listofbadspots.append(myspotlist[i])
	for i in listofbadspots:
		myspotlist.remove(i)
	print myspotlist
	if len(myspotlist)==0:
		return nearestzero(myspot,map)
	distlist=[None]*len(myspotlist)
	for i in range(0,len(distlist)):
		distlist[i]=sqrt((center[0]-myspotlist[i][0])**2+(center[1]-\
		            myspotlist[i][1])**2)
	return myspotlist[distlist.index(max(distlist))]