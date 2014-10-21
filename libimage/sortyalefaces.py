import os

head="subject"
dots=[".centerlight",".glasses",".happy",".leftlight",".noglasses",".normal",".rightlight",".sad",".sleepy",".surprised",".wink"]
for i in range(1,16):
	if i<10:
		thisfile=head+str(0)+str(i)
	else:
		thisfile=head+str(i)
	os.system('mkdir '+thisfile)
	for end in dots:
		try:
			os.system('touch '+thisfile+'/'+thisfile+end)
			os.system('mv '+thisfile+end+' '+thisfile+'/'+thisfile+end)
		except:
			print "something went wrong with "+thisfile+end