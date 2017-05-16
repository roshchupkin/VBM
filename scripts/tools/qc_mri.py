import pandas as pd 
import os
import sys
import matplotlib.pyplot as plt
import numpy as np





src_dir=sys.argv[1]
work_dir=sys.argv[2]
control_path=sys.argv[3]

try:
    mode=sys.argv[4] #TODO smarter way
except:
    mode=None

if mode!='clean':
    try:
        index_names=pd.read_csv(os.path.join(work_dir,'logs', '1.csv'))['0']

    except:
        index_names=pd.read_csv(os.path.join(work_dir,'logs', '0.csv'))['0']


else:
    index_names=pd.read_csv(os.path.join(work_dir,'data_frames', 'clean_mri_list.csv'))['0']

df=pd.DataFrame()

l=os.listdir(control_path)


if 'control.csv' in l:
    df=pd.read_csv( os.path.join(control_path, 'control.csv'), index_col=0)

else:
    #Hammer=pd.read_csv(os.path.join(src_dir, 'standards/atlases/','Hammer_table.csv'),header=None ) [1]

    for i,f in enumerate(l):
        df[i]=pd.read_csv(os.path.join(control_path, f), header=None)[0]

    df.index=index_names
    #df.columns= list(Hammer)
    df.index.name='MRI'

    df.to_csv(os.path.join(control_path, 'control.csv') )




mean=np.mean(df, axis=1)


print '##################################################'
print "The mean percentage of outlier voxels in this study {0}. Should be equal to quantile threshold, what you used for QC, multiplied by 2 (two tails analysis) ".format(np.mean(mean))

print '##################################################'
print 'Check this images! They have too many outliers!!!'
 
print 'index on plot:', list(np.where(np.mean(df, axis=1)>np.mean(mean)+np.std(mean)*3)[0] +1) 
print "Info", mean[np.where(np.mean(df, axis=1)>np.mean(mean)+np.std(mean)*3)[0]]
print '##################################################'
# plt.pcolor(df,cmap=plt.cm.Reds,edgecolors='k')
# plt.colorbar()
# plt.show()
# plt.close()


print "You can use table {0} in {1} for additional analysis.".format('control.csv', control_path)
print "____________________________"
print "For Example in python shell or ipython:"
print "$>import pandas as pd"
print "Read this table by typing in mri_control directory command: $> df=pd.read_csv('control.csv', index_col=0) "
print "Then print summary $> print df.T.describe()"
print "____________________________"
