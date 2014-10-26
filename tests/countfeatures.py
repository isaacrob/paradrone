#based on http://stackoverflow.com/questions/1707620/viola-jones-face-detection-claims-180k-features

framemax=200000
framemin=200000-21
numfeatures=5
listfeatures=[[2,1],[1,2],[3,1],[1,3],[2,2]]
count=0
for i in range(numfeatures):
	sizex=listfeatures[i][0]
	sizey=listfeatures[i][1]
	for x in range(framemin,framemax-sizex+1):
		for y in range(framemin,framemax-sizey+1):
			for width in range(sizex,framemax-x+1,sizex):
				for height in range(sizey,framemax-y+1,sizey):
					count=count+1
print count