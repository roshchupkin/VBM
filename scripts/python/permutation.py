import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import *
import numpy as np
import pandas as pd
from timer import Timer
import argparse
import string
from statistic_methods import GLM
import nipy
from scipy import ndimage


def Exclude_subjects(data_frame, regression_model):

	missed=[]
	for i in regression_model:
		missed=missed + list(np.where( (data_frame[i].isnull()))[0])

	result=np.unique(missed)
	return result

def run_roi_permutation_fast(path_4d, data_table_path, regression_model,
							path_save, atlas, chunk,N_permutation, threshold,test_col,
							 map_type="p-value",perm_type=None, mask=None,type=None,info_table=None):

	id = 'bigrfullname'

	data_frame = pd.read_csv(data_table_path, sep='\t',index_col=None)
	if id not in data_frame.columns:
		data_frame = pd.read_csv(data_table_path, sep=',',index_col=None)
		if id not in data_frame.columns:
			data_frame = pd.read_csv(data_table_path, sep=' ',index_col=None)
			if id not in data_frame.columns:
				print data_frame.columns
				raise ValueError('In data table should be {} column!'.format(id))


	if os.path.isfile(INFO_TABLE[type]):
		mri_order_table=pd.DataFrame.from_csv(INFO_TABLE[type])
		mask=MASK[type]
		atlas=ATLAS[type]
		print INFO_TABLE[type]
		print MASK[type]
		print ATLAS[type]
	else:
		if info_table is None:
			raise ValueError('-sub_list is not defined!')
		if atlas is None:
			raise ValueError('-atlas is not defined!')

	data_frame=data_frame[regression_model+[id]  ].dropna(axis=0)

	data_frame['regression_order']=range(data_frame.shape[0])
	mri_order_table['voxel_order']=range(mri_order_table.shape[0])

	df_result=pd.merge(data_frame,mri_order_table, on='bigrfullname')
	print 'merge...',df_result.shape

	data_frame=df_result[regression_model+[id]]

	Atlas=nipy.load_image(atlas)
	if mask is not None:
		Mask=nipy.load_image(mask)

	map_data=np.zeros(Atlas._data.shape)
	regions=np.array(np.unique(Atlas._data[Atlas._data!=0]), dtype=np.int16)

	statistics=[]

	index=np.where(np.array(regression_model)==test_col)[0][0]+1

	perm_data=np.array(data_frame[test_col].tolist())

	for p in range(N_permutation):
		print p
		np.random.shuffle(perm_data)
		del data_frame[test_col]
		data_frame[test_col]=perm_data

		for r in regions:
			#print r
			data=np.array([])
			reg=-1
			while True:
				reg+=1
				try:
					regression_data=np.load(os.path.join(path_4d,'reg{}_{}.npy'.format(r,reg)))
					regression_data = regression_data[df_result.voxel_order,:]

					p_values, t_stat, b_values = GLM(regression_data, regression_model, data_frame, norm=False)

					if map_type=='p-value':
						p_values=1-p_values
						data=np.append(data,p_values[index,:])
					elif map_type=='t-stat':
						data=np.append(data,t_stat[index,:])
					else:
						raise ValueError('map type {} not implemented'.format(map_type))
				except Exception,e:
					killme=0
					if reg>3:
						break
					else:
						continue
			map_data[Atlas._data==r]=data

		if mask is not None:
			map_data[Mask._data==0]=0
		if perm_type=='cluster':
			if map_type=='t-stat':
				map_data_pos=np.copy(map_data)
				map_data_pos[map_data_pos<0]=0
				map_data[map_data>0]=0
				cluster_map_pos, n_clusters_pos = ndimage.label(map_data_pos > threshold)
				cluster_map_neg, n_clusters_neg = ndimage.label(np.abs(map_data) > threshold)
				print np.sort(np.bincount(cluster_map_neg.ravel())[1:])
				print np.sort(np.bincount(cluster_map_pos.ravel())[1:])
				max=np.max		(
					np.array([
						np.max(np.bincount(cluster_map_neg.ravel())[1:]),
						np.max(np.bincount(cluster_map_pos.ravel())[1:])
							])
								)
				statistics.append(max)
			elif map_type=='p-value':
					cluster_map, n_clusters = ndimage.label(map_data< threshold)
					statistics.append(np.max(np.bincount(cluster_map.ravel())[1:]))
			else:
				raise ValueError('map type {} not implemented'.format(map_type))
		elif perm_type=='max':
			if map_type=='t-stat':
				statistics.append(np.nanmax(map_data))
			elif map_type=='p-value':
				p_min=np.nanmin(map_data[map_data!=0])
				print p_min
				statistics.append(p_min)
			else:
				raise ValueError('map type {} not implemented'.format(map_type))
	np.save(os.path.join(path_save, str(chunk) + "_" + perm_type + "_permutation.npy"), statistics)



def main(args):

	with Timer() as t:
		run_roi_permutation_fast(args.d,args.t, args.r,args.o, args.atlas,args.chunk,int(args.n_perm),
								 args.threshold,args.test_name,args.map_type, perm_type=args.perm_type, mask=args.mask,type=args.type, info_table=args.sub_list)
	print "time to regression %s s" % t.secs


parser = argparse.ArgumentParser(description='Run VBM regression analysis')


parser.add_argument("-o", type=str, help="path to save result folder")
parser.add_argument("-d", type=str, help="path to VBM phenotypes")
parser.add_argument("-t", type=str, help="table with regression parameters")
parser.add_argument('-r', nargs='+', help='regression model', required=True)
parser.add_argument('-atlas', type=str, help='Atlas which was used to split regions')
parser.add_argument('-chunk', required=True, help='')
parser.add_argument('-n_perm', required=True, help='')
parser.add_argument('-threshold',type=np.float64, help='')
parser.add_argument('-map_type',choices=['p-value','t-stat'], required=True, help='')
parser.add_argument('-test_name', required=True, help='')
parser.add_argument('-perm_type', required=True, choices=['cluster','max'], help='')
parser.add_argument('-mask',type=str, help='binary mask for counting permutation inside it')
parser.add_argument('-sub_list',type=str, help='csv table with one column of subject ids')
parser.add_argument("-type", type=str,required=True,choices=["GM","WM","FA","MD"], help="MRI data type for regression")
args = parser.parse_args()
print args

if args.threshold is None and args.perm_type=='cluster':
	raise ValueError('For cluster permutation -threshold parameter is required!')

main(args)
