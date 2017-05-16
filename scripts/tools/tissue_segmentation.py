

import sys
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/plot_brain/')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/Tools/')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/MRI_project/')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/Profilers/')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/Genetic/')
# sys.path.append('/scratch/groshchupkin/python_scripts/ubuntu_32/Regression/')

sys.path.append('/scratch/groshchupkin/RotterdamStudy/packages/vbm/scripts/tools/')
sys.path.append('/scratch/groshchupkin/RotterdamStudy/packages/vbm/scripts/python/')

import os
import nipy
import numpy as np
from .python.timer import Timer
import argparse

def tissue_segmentation(save_path,image_path,segmentation_path,type, save_mask):

	seg_dic={'GM':2,'WM':3,'CSF':1,'brain':0}

	name=type + '_' + os.path.basename(image_path)

	Segm=nipy.load_image(segmentation_path)

	if type!='brain':
		tissue_code=seg_dic[type]
		mask=np.where(Segm._data!=tissue_code)
	elif type=='brain':
		mask=np.where(Segm._data==0)

	if save_mask=='n':
		Image=nipy.load_image(image_path)
		Image._data[mask]=0
		nipy.save_image(Image, os.path.join(save_path, name))

	else:
		Segm._data[mask]=0
		Segm._data[Segm._data!=0]=1
		nipy.save_image(Segm, os.path.join(save_path, 'mask_'+name))


parser = argparse.ArgumentParser(description='Tissue segmentation')
parser.add_argument("-o",required=True, type=str, help="path to save result folder")
parser.add_argument("-i",required=True, type=str, help="input image")
parser.add_argument("-s",required=True, type=str, help="segmentation mask")
parser.add_argument("-type",required=True, type=str,choices=['GM','WM','CSF','brain'], help="segmentation type")
parser.add_argument("-m",choices=['y','n'],type=str, help="save mask or tissue")
args = parser.parse_args()
print args


if __name__=="__main__":

	with Timer() as t:
		tissue_segmentation(args.o, args.i, args.s,args.type, args.m)
	print "=> time: for segmentation  %s s" %(t.secs)
    

