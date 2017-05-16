import numpy as np 
import os
import sys
import nipy


def load_data(data_path, region_code):
        
    region_data=[]
    
    p=1
    
    while True:                
        try:
            region_data.append(np.load( os.path.join(data_path, 'reg'+region_code +'_'+str(p) + ".npy" ) ) )
            #region_data.append(np.load( os.path.join(data_path, str(region_code) +'_'+str(p) + ".npy" ) ) )
            p+=1
        except:
            break

    region_data=np.concatenate(region_data, axis=1)
    
    return region_data




def check_denstity(region_data, tissue_threshold):
    
    median=np.apply_along_axis(np.median, 0, region_data)

    include=np.where(median>tissue_threshold)

    return include   



src_dir=sys.argv[1]
work_dir=sys.argv[2]
data_path=sys.argv[3]
tissue_threshold=float(sys.argv[4])


Atlas=nipy.load_image(os.path.join(src_dir,'standards/atlases/Hammer_1mm_MNI.nii.gz'))


region_codes=np.unique(Atlas._data)

region_codes=region_codes[region_codes!=0]

region_coodinates={i:np.where(Atlas._data==i) for i in region_codes}


for c in region_codes:
    print c
    coordinates=region_coodinates[c]
    Atlas._data[coordinates]=0

    region_data=load_data(data_path, c)
    include=check_denstity(region_data, tissue_threshold)

    Atlas._data[coordinates[0][include], coordinates[1][include] , coordinates[2][include]]=1


nipy.save_image(Atlas, os.path.join(work_dir, 'study_mask_' + str(tissue_threshold) + '.nii.gz') )








