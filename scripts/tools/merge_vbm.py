import os
import sys
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Run VBM regression analysis')

parser.add_argument("-roi",  required=True,type=str, help="ROI name")
parser.add_argument("-o", "--out", required=True, type=str, help="path to save result folder")
parser.add_argument("-d", "--data",nargs='+',  required=True, type=str, help="path to VBM phenotypes")
parser.add_argument('-sub_list',nargs='+',type=str,default=None,  required=False, help='csv tables with one column of subject ids per VBM phenotype')

args = parser.parse_args()
print args


if len(args.data)!=len(args.sub_list):
	raise ValueError('Input number of phenotypes folder should be the same as number of input subject tables')

d=None
for i in args.data:
	if not os.path.isfile('{}/{}'.format(i,args.roi)):
		raise ValueError('File {}/{} does not exist'.format( i,args.roi ))

	else:
		d=np.load('{}/{}'.format(i,args.roi)) if d is None else np.vstack([d, np.load('{}/{}'.format(i,args.roi)) ])
		print d.shape


if args.sub_list is not None:

	df_ids=None
	for i in args.sub_list:
		if not os.path.isfile('{}'.format(i)):
			raise ValueError('File {} does not exist'.format( args.sub_list ))

		else:
			df_ids=pd.read_csv(i) if df_ids is None else df_ids.append(pd.read_csv(i))
			print df_ids.shape

	if d.shape[0]!=df_ids.shape[0]:
		raise ValueError("Number of images {} is different from number of ids {}!!!".format(d.shape[0], df_ids.shape[0]))
	df_ids.to_csv('{}/ids_list.csv'.format(args.out), index=None)



np.save("{}/{}".format(args.out,args.roi),d)

