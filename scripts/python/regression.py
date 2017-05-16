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

def run_roi_regression_fast(path_4d, roi_code, data_table_path, data_table_name, regression_model,
							path_save, id):
	print roi_code


	if data_table_name[-3:] == 'csv':
		data_frame = pd.DataFrame.from_csv(os.path.join(data_table_path, data_table_name), sep='\t')
	else:
		raise('Info table should be .csv')


	regression_data = np.load(os.path.join(path_4d, 'reg' + roi_code + ".npy"))

	info_table=pd.DataFrame.from_csv(os.path.join(data_table_path,data_table_name),index_col=False)

	if os.path.isfile(os.path.join(data_table_path, 'dir_list.csv')): #TODO change to normal name
		mri_order_table=pd.DataFrame.from_csv(os.path.join(data_table_path, 'dir_list.csv'))
		name_order=[]
		for i in mri_order_table['0']:
			name_order.append(string.split(i,'_s3')[0]) #TODO 's3' should be standard

	else:
		raise("There is no info about mri order, need mri order file!")


	#exclude_index=Exclude_subjects(data_frame, regression_model)
	#print (exclude_index)


	data_frame=data_frame[regression_model+[id]  ].dropna(axis=0)

	reorder_index=[]
	del_subjects=[]


	for i,j in enumerate(name_order):
		try:
			reorder_index.append(data_frame[data_frame[id]==j].index[0])
		except:
			del_subjects.append(i)

	reorder_index=np.array(reorder_index)
	print reorder_index
	data_frame=data_frame.reindex(reorder_index)

	del_subjects=np.array(del_subjects)

	print regression_data.shape

	if len(del_subjects)!=0:
		regression_data = np.delete(regression_data, del_subjects, axis=0)

	regression_data[np.where(np.isnan(regression_data))] = 0
	regression_data[np.where(np.isinf(regression_data))] = 0

	print regression_data.shape
	print data_frame.shape
	p_values, t_stat, b_values = GLM(regression_data, regression_model, data_frame, norm=False)

	np.save(os.path.join(path_save, roi_code + "_p_values"), p_values)
	np.save(os.path.join(path_save, roi_code + "_t_stat"), t_stat)
	np.save(os.path.join(path_save, roi_code + "_b_values"),b_values)

#########################################rs77956314_T###################################


def main(data_table_path, data_table_name, regression_model, path_4d, roi_code, path_save, id):
	with Timer() as t:
		run_roi_regression_fast(path_4d, roi_code, data_table_path, data_table_name, regression_model,
								path_save, id)
	print "time to regression %s s" % t.secs


parser = argparse.ArgumentParser(description='Run VBM regression analysis')

parser.add_argument("-roi", type=str, help="path to mask folder")
parser.add_argument("-o", "-out", type=str, help="path to save result folder")
parser.add_argument("-d", "-data", type=str, help="path to VBM phenotypes")
parser.add_argument("-t", "-tables", type=str, help="path to table folder")
parser.add_argument("-info", type=str, help="info table name")
parser.add_argument('-r','--regression', nargs='+', help='regression model', required=True)
parser.add_argument("-id", type=str, help="column name for subjects id")

args = parser.parse_args()
#print args


main(args.t, args.info, args.regression, args.d, args.roi, args.o, args.id)
