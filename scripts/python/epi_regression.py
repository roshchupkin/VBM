import os
import sys
import statsmodels.api as sm
from statsmodels.formula.api import ols
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


def Exclude_subjects(data_frame, regression_model):

	missed=[]
	for i in regression_model:
		missed=missed + list(np.where( (data_frame[i].isnull()))[0])

	result=np.unique(missed)
	return result


def merge_roi(path_4d,roi_code):

	data=[]
	reg=-1
	while True:
		reg+=1
		try:
			regression_data=np.load(os.path.join(path_4d,'reg{}_{}.npy'.format(roi_code,reg)))
			data.append(regression_data)
		except:
			if reg!=10:
				break
			else:
				continue

	data=np.concatenate(data,axis=1)

	return data

def run_roi_regression_fast(path_4d, roi_code, data_table_path, regression_model,
							path_save, type, info_table=None):
	print roi_code


	separator=['\t',',',';']

	for s in separator:
		data_frame = pd.DataFrame.from_csv(data_table_path, sep=s, index_col=None)
		if 'bigrfullname' in data_frame.columns:
			id = 'bigrfullname'
			break
	else:
		print data_frame.columns
		raise ValueError('In data table should be bigrfullname column!')


	data_frame=data_frame.replace(r'\s+', np.nan, regex=True).replace('',np.nan)
	data_frame = data_frame[regression_model + [id]].dropna(axis=0)

	if len(string.split(roi_code,'_'))==2:
		regression_data = np.load(os.path.join(path_4d, 'reg' + roi_code + ".npy"))

	elif len(string.split(roi_code,'_'))==1:
		regression_data=merge_roi(path_4d,roi_code)

		if os.path.isfile(INFO_TABLE[type]):
			mri_order_table=pd.DataFrame.from_csv(INFO_TABLE[type])
		else:
			raise ValueError('-sub_list is not defined!')

	data_frame=data_frame[regression_model+[id]  ].dropna(axis=0)

	print regression_data.shape
	print data_frame.shape
	data_frame['regression_order']=range(data_frame.shape[0])
	mri_order_table['voxel_order']=range(mri_order_table.shape[0])

	df_result=pd.merge(data_frame,mri_order_table, on='bigrfullname')
	print 'merge...',df_result.shape
	print df_result.head()



	regression_data = regression_data[df_result.voxel_order,:]

	data_frame=df_result[regression_model+[id]]
	#TODO check this
	null=data_frame.isnull()
	null=null.as_matrix()
	print np.sum(null)
	if np.sum(null)!=0:
		print 'There are {} missed values in table'.format(np.sum(null))
		null_subjects=np.where(np.sum(null,axis=0)!=0)
		data_frame=data_frame.drop(null_subjects, axis=0)
		regression_data = np.delete(regression_data, null_subjects, axis=0)

	data_frame.to_csv(os.path.join(path_save, 'merged_df.csv'))
	data_frame[regression_model]=data_frame[regression_model].astype(np.float64)

	print 'Y shape: #subjects-{}; #voxels-{}'.format(regression_data.shape[0],regression_data.shape[1])
	print 'X shape: #subjects-{}; #covariates-{}'.format(data_frame.shape[0],str(data_frame.shape[1]-1))
	print 'Regession Model: Y ~ intercept+',regression_model

	p_values, t_stat, b_values = GLM(regression_data, regression_model, data_frame, norm=False)

	name=roi_code
	np.save(os.path.join(path_save, name + "_p_values"), p_values)
	np.save(os.path.join(path_save, name + "_t_stat"), t_stat)
	np.save(os.path.join(path_save, name + "_b_values"),b_values)

#########################################rs77956314_T###################################


def main(args):

	with Timer() as t:

		run_roi_regression_fast(args.d,args.roi ,args.t, args.regression,args.o,args.type, info_table=args.sub_list)

	print "time to regression %s s" % t.secs


parser = argparse.ArgumentParser(description='Run VBM regression analysis')

parser.add_argument("-roi", type=str, help="ROI name")
parser.add_argument("-o", "-out", type=str, help="path to save result folder")
parser.add_argument("-d", "-data", type=str, help="path to VBM phenotypes")
parser.add_argument("-t", "-table", type=str, help="table with regression parameters")
parser.add_argument("-type", type=str,choices=["GM","WM","FA",'FLAIR','MD','CON_DEN','CON_MAX'], help="MRI data type for regression")
parser.add_argument('-r','--regression', nargs='+', help='regression model', required=True)
parser.add_argument('-sub_list',type=str, help='csv table with one column of subject ids')


args = parser.parse_args()
print args


main(args)
