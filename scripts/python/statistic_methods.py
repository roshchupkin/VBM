#!/bin/env python

import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn import linear_model
from scipy import stats
import numpy as np
from sklearn.preprocessing import normalize




def linear_regression (voxel_values, regressor_names, data_frame):

	s=pd.Series(voxel_values)

	data=data_frame[regressor_names]

	data['voxel']=s

	model_string=' + '.join(regressor_names)

	results = ols("%s ~ %s" %("voxel", model_string), data=data).fit()

	return results.pvalues, results.params




def GLM(voxel_values, regressor_names, data_frame, norm=False, Xdata=None, n_j=-1):

	regr = linear_model.LinearRegression(fit_intercept=False)


	'''
	 X : numpy array or sparse matrix of shape [n_samples,n_features]
			Training data
	 Y : numpy array of shape [n_samples, n_targets]
	'''
	Y=np.array(voxel_values)

	if not isinstance(Xdata, type(None)):
		X=Xdata
	else:
		X=np.array(data_frame[regressor_names])


	X = sm.add_constant(X)    #TODO add parameter intercept

	if norm:
		X=normalize(X, norm='l2', axis=0)

	regr.fit(X, Y)

	squared_residuals=regr.residues_


	sse = squared_residuals / float(X.shape[0] - X.shape[1] )
	# 1/(N-p-1) but 1 is insight X because we add intercept



	se = np.array([
					  np.sqrt( sse *np.diagonal( np.linalg.inv(np.dot(X.T, X)))[i] )
					  for i in range(X.shape[1])
					  ])

	coef=np.array(regr.coef_)
	sse=np.array(sse)
	se=np.array(se)


	t = np.array([   coef[:,i] /se[i,:] for i in range(coef.shape[1])    ])


	DF=(Y.shape[0] - X.shape[1])

	number_coef=coef.shape[1]

	#p = np.array(   [   2 * (1 - stats.t.cdf(np.abs(t[i,:]), DF  )) for i in range(number_coef)   ]    )
	p = np.array(   [   2 * (stats.t.sf(np.abs(t[i,:]), DF  )) for i in range(number_coef)   ]    )


	return p , t , coef


            
            
            
            
            
            
            
