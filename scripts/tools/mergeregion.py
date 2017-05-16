

import os
import numpy as np
import sys



def merge(data_path, code ,pattern):

    p=0

    values=[]
    while True:
        try:

            loaded=np.load(os.path.join(data_path, str(code)+'_'+str(p)+'_'+ pattern + '.npy') )
            p+=1
            values.append( loaded )
        except:
            break
    d=np.concatenate(values, axis=1)
    np.save(os.path.join(data_path, str(code)+ '_'+ pattern + '.npy'), d)


if __name__=="__main__":
    merge(sys.argv[1], sys.argv[2], sys.argv[3])