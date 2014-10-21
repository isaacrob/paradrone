import os

head="subject"
dots=[".centerlight",".glasses",".happy",".leftlight",".noglasses",".normal",".rightlight",".sad",".sleepy",".surprised",".wink"]
for i in range(1,16):
	if i<10:
		thisfile=head+str(0)+str(i)
	else:
		thisfile=head+str(i)
	for j in range(len(dots)):
		try:
			os.system('mv '+thisfile+'/'+thisfile+dots[j]+' '+thisfile+'/'+str(i+1))
		except:
			print "something went wrong"