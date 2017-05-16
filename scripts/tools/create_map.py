import nipy
import numpy as np
import argparse
import os
import re


def merge_roi(path_4d,r, index,type ):

	data=[]
	reg=-1
	while True:
		reg+=1
		try:
			if type in ['p_log']:
				d=list(-np.log10((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,'p_values')))[index,:])))
			elif type=='se':
				d1=(((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,'b_values')))[:,index])))
				d2=(((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,'t_stat')))[index,:])))
				d=list(d1/d2)
			elif type=='b_values':
				d=list((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,type)))[:,index]))
			elif type in ['p_values','p_values_inv']:
				d=list((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,'p_values')))[index,:]))
				if len(d)==0:
					continue
			else:
				d=list((np.load(os.path.join(path_4d, '{}_{}_{}.npy'.format(r,reg,type)))[index,:]))

			data=data + d
		except:
			if reg>3:
				break
			else:
				continue

	if len(data)==0:
			try:
				if type in ['p_log']:
					d=list(-np.log10((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,'p_values')))[index,:])))
				elif type=='se':
					d1=(((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,'b_values')))[:,index])))
					d2=(((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,'t_stat')))[index,:])))
					d=list(d1/d2)
				elif type=='b_values':
					d=list((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,type)))[:,index]))
				elif type in ['p_values','p_values_inv']:
					d=list((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,'p_values')))[index,:]))
				else:
					d=list((np.load(os.path.join(path_4d, '{}_{}.npy'.format(r,type)))[index,:]))

				data=data + d
			except:
				print ('There is no results for rio {}'.format(r))

	return data




parser = argparse.ArgumentParser(description='Script to make map of results in MNI space')

parser.add_argument("-i", type=str, help="path to regression results")
parser.add_argument("-o", "--out", type=str, help="path to save result folder")
parser.add_argument("-t", "--template", type=str, help="path to template brain")
parser.add_argument("-type", type=str,choices=['p_values','p_values_inv','t_stat','b_values','p_log','se'], help="map type")
parser.add_argument("-a", type=str, help="path to Atlas")
parser.add_argument("-index", type=int, help="covariate index")
parser.add_argument("-n","--name", type=str, help="save name")
parser.add_argument("-mask", type=str, help="path to mask")


args = parser.parse_args()
print args

Template=nipy.load_image(args.template)
Atlas=nipy.load_image(args.a)

mask=None

if args.mask:
	Mask=nipy.load_image(args.mask)
	mask=np.where(Mask._data==0)

map_data=np.zeros(Template._data.shape)

regions=np.array(np.unique(Atlas._data[Atlas._data!=0]), dtype=np.int16)

files=os.listdir(args.i)

for r in regions:
	print r
	data=merge_roi(args.i,r, args.index,args.type )

	data=np.array(data)

	if args.type=='p_values_inv':
		data=1-data
		map_data[Atlas._data==r]=data
	else:
		map_data[Atlas._data==r]=data


if mask:
	map_data[mask]=0

if args.type=='t_stat':
	neg_mask=np.where(map_data<0)
	pos_mask=np.where(map_data>0)
	map_data=np.abs(map_data)


	Template._data[:,:,:]=0
	Template._data[neg_mask]=map_data[neg_mask]
	#Template._data[mask]=0
	#Template.header['cal_max']=np.max(Template._data)
	nipy.save_image(Template,os.path.join(args.out, 'neg_'+args.name )  )



	Template._data[:,:,:]=0
	Template._data[pos_mask]=map_data[pos_mask]
	#Template._data[mask]=0
	#Template.header['cal_max']=np.max(Template._data)
	nipy.save_image(Template,os.path.join(args.out, 'pos_'+args.name )  )





else:
	Template._data=map_data


	Template.header['cal_max']=np.nanmax(Template._data)
	nipy.save_image(Template,os.path.join(args.out, args.name ) )
	if args.type=='p-values_inv':
		print ('Map was saved with (1-Pvalue) values!')







