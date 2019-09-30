import os
import sys
import numpy as np
import pandas as pd
import argparse
import scipy
import nipy


def nifti_ma(beta, se):
	if len(beta) != len(se):
		raise ValueError('Different number of sites with SE and Beta')
	sum_w = 0
	sum_Bw = 0

	for i in range(len(beta)):
		# x,y,z=beta[i].shape

		w = 1.0 / np.power(se[i], 2)
		Bw = beta[i] * w

		sum_w += w
		sum_Bw += Bw

	Beta = sum_Bw / sum_w
	SE = np.sqrt(1.0 / sum_w)
	Z = Beta / SE

	p_values = scipy.stats.norm.sf(abs(Z)) * 2  # twosided

	return Beta, SE, Z, p_values


parser = argparse.ArgumentParser(description='Run VBM inverse-variance Meta-analysis')
parser.add_argument("-se",nargs='+',  required=True, type=str, help="paths to se maps")
parser.add_argument("-beta",nargs='+',  required=True, type=str, help="paths to beta maps")
parser.add_argument("-template", required=True, type=str, help="path to MNI template")
parser.add_argument("-out", required=True, type=str, help="path to save results")

args = parser.parse_args()
print args


if len(args.se)!=len(args.beta):
	raise ValueError('different number of SE maps and BETA maps!!!')

N=len(args.se)


SE={}
Beta={}

for i in range(N):
	SE[i] = nipy.load_image(args.se[i])._data
	Beta[i] = nipy.load_image(args.beta[i])._data

b, se, z, p = nifti_ma(Beta, SE)

T = nipy.load_image(args.template)

T._data[:, :, :] = 0
T._data = p
m=np.isnan(T._data)
print "{} NaNs".format(m.sum())
T._data[m]=1
nipy.save_image(T,'{}/ma_p_value.nii.gz'.format(args.out))


T._data[:, :, :] = 0
T._data = b
m=np.isnan(T._data)
print "{} NaNs".format(m.sum())
T._data[m]=0
nipy.save_image(T,'{}/ma_beta.nii.gz'.format(args.out))


T._data[:, :, :] = 0
T._data = se
nipy.save_image(T,'{}/ma_SE.nii.gz'.format(args.out))
