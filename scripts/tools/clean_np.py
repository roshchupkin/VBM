import numpy as np 
import os
import sys
import pandas as pd



work_dir=sys.argv[1]
delete_images=sys.argv[2]
save_path=sys.argv[3]

df_del=list(pd.read_csv(delete_images, header=None) [0] )

mri_list=list(pd.read_csv(os.path.join(work_dir,'logs', '0.csv'))['0'])

delete=[]

for i in df_del:

	delete.append(mri_list.index(i))



l=os.listdir(os.path.join(work_dir, 'nparray'))

for d in l:

	print d

	data=np.load(os.path.join(work_dir, 'nparray', d))

	data=np.delete(data,delete, axis=0)


	np.save(os.path.join(save_path, d), data)


clearn_mri=np.delete(mri_list,delete)

clearn_mri=pd.DataFrame(clearn_mri)

clearn_mri.to_csv(os.path.join( work_dir,'data_frames','clean_mri_list.csv') )

