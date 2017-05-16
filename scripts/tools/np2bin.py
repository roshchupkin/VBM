
import numpy as np 
import sys
import os
import string
import struct

def converter_np2r(d, name, data_save):

    
    
    save_name='data'+name + ".bin"

           
    # create a binary file                    
                        
    binfile = file(os.path.join(data_save,save_name), 'wb')                   
  
  	# and write out two integers with the row and column dimension
                    
    header = struct.pack('2I', d.shape[0], d.shape[1])
    binfile.write(header)
    # then loop over columns and write each
    for i in range(d.shape[1]):
        data = struct.pack('%id' % d.shape[0], *d[:,i])
        binfile.write(data)
    binfile.close()




if __name__=="__main__":


    data_path=sys.argv[1]
    data_save=sys.argv[2]

    name=string.split(os.path.basename(data_path),'.npy' )[0]

    d=np.load(data_path)

    converter_np2r(d, name, data_save)

