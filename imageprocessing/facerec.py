import cv2, sys, os
import numpy as np

#initialize the cascade
pathtocascade=raw_input("path to haarcascade: ")
try:
	facecascade=cv2.CascadeClassifier(pathtocascade)
except:
	sys.exit("failed to load cascade")
print "initialized haarcascade "

#initialize the face recognizer
myrec=