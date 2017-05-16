import nipy
import pandas as pd
import numpy as np
import argparse
import os
from collections import OrderedDict
import sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
from config import *

parser = argparse.ArgumentParser(description='Script to create summary of VBM experiment.'
											 'Summary table:'
											 'Brain Region,Region size (#voxels),min p-value,# negative voxels,# positive voxels ')

parser.add_argument("-p",required=True, type=str, help="p-map image (with real p-values, not (1-p_value)!)")
parser.add_argument("-t",required=True, type=str, help="t-map or b-map image")
parser.add_argument("-a", type=str,default='Hammer',choices=['Hammer','FreeSurfer','Tracts'], help="Atlas name")
parser.add_argument("-o",required=True, type=str, help="output folder")
parser.add_argument("-n",required=True, type=str, help="result table name")
parser.add_argument("-th",required=True, type=float, help="p-value threshold")
parser.add_argument("-mask",default=None, type=str, help="path mask image")
parser.add_argument("-atlas",default=None, type=str, help="path atlas image")
parser.add_argument("-tract_th", type=float, default=0.0, help='tracts threshold for minimum probability to include voxel')

args = parser.parse_args()
print args


def get_atlas(atlas_name,atlas_path):
	Atlas={}
	Atlas['mask']={}
	Atlas['regions']={}

	if atlas_path is None:
		Atlas_path=ATLAS[atlas_name]
	else:
		Atlas_path = atlas_path
	Atlas_table=INFO_TABLE[atlas_name]


	A=nipy.load_image(Atlas_path)
	Table=pd.read_csv(Atlas_table, sep=',', header=None)

	if atlas_name!='Tracts':
		u=np.unique(A._data)
		for j,i in enumerate(Table[0]):
			if i in u:
				Atlas['regions'][i]=Table[1][j]
				Atlas['mask'][i]=np.where(A._data==i)
		return Atlas

	else:
		Atlas['mask']=A
		Atlas['regions']=Table[1].tolist()
		return Atlas


if __name__=="__main__":

	if args.th<=0 or args.th>=1:
		raise ValueError('Threshold should be 0 < threshold < 1, not {}'.format(args.th))

	results=OrderedDict()
	Atlas=get_atlas(args.a, args.atlas)
	P=nipy.load_image(args.p)
	if args.mask is not None:
		M=nipy.load_image(args.mask)
		P._data[M._data==0]=1


	results['Brain Region']=[]
	results['Region size (#voxels)']=[]
	results['min p-value']=[]
	results['# negative voxels']=[]
	results['# positive voxels']=[]

	mask=np.where(P._data>args.th)
	P._data[mask]=1
	P._data[P._data==0]=1 #TODO change:check with mask, if zero outside, then it is significant


	T_neg=nipy.load_image(args.t)
	T_pos=nipy.load_image(args.t)
	T_neg._data[mask]=0
	T_pos._data[mask]=0
	T_pos[T_pos._data<0]=0
	T_neg[T_neg._data>0]=0

	if args.a!='Tracts':
		for k in Atlas['mask']:
			results['Brain Region'].append(Atlas['regions'][k])
			results['Region size (#voxels)'].append( len(Atlas['mask'][k][0]) )
			results['min p-value'].append(np.min( P._data[Atlas['mask'][k]] ))
			results['# negative voxels'].append(len(  np.where(T_neg._data[Atlas['mask'][k]]!=0)[0] ))
			results['# positive voxels'].append(len(  np.where(T_pos._data[Atlas['mask'][k]]!=0)[0] ))

	else:
		for j,i in enumerate(Atlas['regions']):
			results['Brain Region'].append(i)
			tract=Atlas['mask'][:,:,:,j+1] #Tract atlas starts from 0 dim with no info
			#print i, tract.shape, args.tract_th
			tract_mask=np.where(tract._data>args.tract_th)
			#print tract_mask[0]
			results['Region size (#voxels)'].append(  len(tract_mask[0]) )
			results['min p-value'].append(np.min(P._data[tract_mask]))
			results['# negative voxels'].append(len(np.where(T_neg._data[tract_mask] != 0)[0]))
			results['# positive voxels'].append(len(np.where(T_pos._data[tract_mask] != 0)[0]))





	df=pd.DataFrame.from_dict(results)
	df.to_csv(os.path.join(args.o,args.n), sep=',', index=False)





