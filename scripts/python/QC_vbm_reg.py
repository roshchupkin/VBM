import sys
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def load_data(data_path, region_code):
    region_data=[]
    p=0
    while True:
        try:
            region_data.append(np.load( os.path.join(data_path, 'reg'+str(region_code) +'_'+str(p) + ".npy" ) ) )
            p+=1
        except:
            break
    region_data=np.concatenate(region_data, axis=1)
    return region_data


def region_quantile(region_data):
    return np.percentile(region_data, range(1,100,1))


def detect_bad_mri (quantile, region_data, settings):
    mri_numbers, voxels_numbers=region_data.shape
    Min=quantile[settings[0]-1]
    Max=quantile[settings[1]-1]
    r1=np.array([len(np.where(region_data[i,:]<Min)[0])/float(voxels_numbers) for i in xrange(mri_numbers) ])
    r2=np.array([len(np.where(region_data[i,:]>Max)[0])/float(voxels_numbers) for i in xrange(mri_numbers) ])
    result=r1+r2
    return result

def check_denstity(region_data, tissue_threshold):
    median=np.apply_along_axis(np.median, 0, region_data)
    include=np.where(median>tissue_threshold)
    return include


def region_summary(data_path, region_code, quantile_threshold, tissue_threshold):

    region_data=load_data(data_path, region_code)
    print 'region code {0}'.format(region_code)
    print 'region size {0}'.format(region_data.shape)

    if isinstance(tissue_threshold, type(None)):
        pass
    else:
        include=check_denstity(region_data, tissue_threshold)
        region_data=region_data[:,include[0]]
        print 'regions size after tissue threshold {0} '.format(region_data.shape)

    q=region_quantile(region_data)
    settings=[quantile_threshold,100-quantile_threshold]

    mri=detect_bad_mri(q, region_data, settings)

    return mri


def qc_summary(work_dir,control_path,quantile_threshold):

    index_names=pd.read_csv(os.path.join(work_dir, '1.csv'))['0']

    df=pd.DataFrame()
    l=os.listdir(control_path)

    if 'control.csv' in l:
        df=pd.read_csv( os.path.join(control_path, 'control.csv'), index_col=0)

    else:
        for i,f in enumerate(l):
            df[i]=pd.read_csv(os.path.join(control_path, f), header=None)[0]

        df.index=index_names
        df.index.name='MRI'
        df.to_csv(os.path.join(control_path, 'control.csv') )

    mean=np.mean(df, axis=1)

    print '##################################################'
    print "The mean percentage of outlier voxels in this study {0}. " \
          "Should be less then quantile threshold {1} multiplied by 2 (two tails analysis) ".format(np.mean(mean)*100,quantile_threshold)

    outlier_index=list(np.where(mean>np.mean(mean)+np.std(mean)*3)[0])

    if len(outlier_index)!=0:
        print '##################################################'
        print 'Check this images! They have too many outliers! Info save to {}'.format(os.path.join(control_path,'outlier_mri_id.csv'))
        print "Info", mean[np.where(mean>np.mean(mean)+np.std(mean)*3)[0]]

        outlier_mri_id=[ i for i in mean[outlier_index].index.tolist()]
        pd.DataFrame.from_dict({'mri':outlier_mri_id,'outlier proportion':mean[outlier_index] } ).to_csv(os.path.join(control_path,'outlier_mri_id.csv'))
    else:
        print "There is no outliers."

    print '##################################################'
    print "You can use table {0} in {1} for additional analysis." \
          " Rows are image names, columns - chunk number. Cell value = The percentage of outlier voxels in chunk.".format('control.csv', control_path)
    print "____________________________"
    print "For Example in python shell or ipython:"
    print "$>import pandas as pd"
    print "Read this table by typing in mri_control directory command: $> df=pd.read_csv('control.csv', index_col=0) "
    print "Then print summary $> print df.T.describe()"
    print "____________________________"





if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Quality Control of VBM results based on converted nparrays')
    parser.add_argument("-o",required=True, type=str, help="path to save result folder")
    parser.add_argument("-i",required=True, type=str, help="path to nparrays")
    parser.add_argument("-code",type=int, help="Atlas chunk code")
    parser.add_argument("-q",required=True,type=int, help="quantile threshold")
    parser.add_argument("-t",type=int, help="tissue threshold")
    parser.add_argument("-logs",type=str, help="path to saved logs from converting stage")
    parser.add_argument("-mode",type=str,choices=['region','summary'],help="mode of QC analysis")


    args = parser.parse_args()
    print args
    data_path=args.i
    region_code=args.code
    save_path=args.o
    quantile_threshold=args.q
    tissue_threshold=args.t

    if args.mode=='region':
        mri=region_summary(data_path, region_code, quantile_threshold, tissue_threshold )
        np.savetxt(os.path.join(save_path, str(region_code) + '.csv'), mri, delimiter=" ")

    elif args.mode=='summary':
        qc_summary(args.logs,args.o,quantile_threshold)



