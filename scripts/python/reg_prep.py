import sys
from timer import Timer
import os
import numpy as np



def convert_array_for_regression(path_4d, region_code):   
    
    regression_data=[]    
    p=1    
    while True:                
        try:
            regression_data.append(np.load( os.path.join(path_4d, region_code +'_'+str(p) + ".npy" ) ) )
            
            p+=1
        except:
            break
    
    regression_data=np.concatenate(regression_data)

       
    sample_size, number_voxels=regression_data.shape
    
    
    split_size=1000
    
    d=number_voxels/split_size
    
    r=number_voxels-d*split_size
    
    
    if d!=0:
    
        l=[range(split_size*i,split_size*(i+1)) for i in range(0,d) ]
        
        
        for i,j in enumerate(l):        
            save_np=regression_data[:,j]
            np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(i)) ,  save_np )
            
        
        save_np=regression_data[:,d*split_size:d*split_size+r]
        np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(i+1)) ,  save_np )
        
    else:
        np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(1)) ,  regression_data )
    
    


if __name__=="__main__":   
    
    arg=sys.argv 

    with Timer() as t:
        convert_array_for_regression(arg[1], arg[2])        
    print "time for split array %s s" %(t.secs)
     
    
