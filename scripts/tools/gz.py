import nipy
import sys
import string


if len(sys.argv)>2:
	raise Exception('Only one argument needed! (Image pathway)') 

name=string.split(sys.argv[1], '.')

if name[-1]!='nii':
	raise Exception('Only unzipped .nii format possible... ')


I=nipy.load_image(sys.argv[1])


nipy.save_image(I, sys.argv[1]+'.gz')



