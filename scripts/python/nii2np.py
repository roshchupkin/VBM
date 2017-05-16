import sys
from timer import Timer
import os
import pandas as pd
import nipy
import numpy as np
import re
import argparse


def get_images_list(path, regexp, number_images=None):

    im_list=[]
    dir_list=os.listdir(path)
    if regexp=="NO":
        im_list=dir_list
        return dir_list

    reg=re.compile(regexp)
    im_list=[i for i in dir_list for m in [reg.search(i)] if m]
    if isinstance(number_images, type(None) ):
        if len(im_list)!=int(number_images):
            raise Exception("set numbers of images have to be the same with numbers images in directory!")
    return im_list


def delete_arrays(path_4d, region_code):
    '''delete temporal arrays '''
    p=1
    while True:
        if os.path.isfile( os.path.join(path_4d, str(region_code) +'_'+str(p) + ".npy" ) ):
            os.remove(os.path.join(path_4d, str(region_code) +'_'+str(p) + ".npy" ))
            p+=1
        else:
            break


def convert_array_for_regression(path_4d, region_code, split_size=1000):
    ''' merge region array to one and split it in (number images in study) x (voxels split_size) '''

    regression_data=[]
    p=1
    while True:
        try:
            regression_data.append(np.load( os.path.join(path_4d, str(region_code) +'_'+str(p) + ".npy" ) ) )
            print str(region_code) +'_' +str(p) + ".npy"
            p+=1
        except:
            break

    regression_data=np.concatenate(regression_data)
    print "Region {}, regression data size {}, will be split by {} voxels chunks ".format(region_code,regression_data.shape, split_size)
    sample_size, number_voxels=regression_data.shape
    d=number_voxels/split_size
    r=number_voxels-d*split_size

    if d!=0:

        l=[range(split_size*i,split_size*(i+1)) for i in range(0,d) ]

        for i,j in enumerate(l): # TODO start from 0, maybe change to 1
            save_np=regression_data[:,j]
            np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(i)) ,  save_np )

        if r!=0:
            save_np=regression_data[:,d*split_size:d*split_size+r]
            np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(i+1)) ,  save_np )
    else:
        np.save(os.path.join(path_4d, 'reg' + str(region_code) + "_" + str(0)) ,  regression_data )


def save_4d_data(Hammer_atlas, image_path, path_4d, image_names):
    '''produce nparrays  (voxels in region) x (image in study)
    only if number of images less then 1000
    '''


    region_codes=np.unique(Hammer_atlas._data)
    region_codes=region_codes[region_codes!=0]
    region_coodinates={i:np.where(Hammer_atlas._data==i) for i in region_codes}
    data_4d={i:[] for i in region_codes}

    for im in image_names:
        print im
        try:
            images_data=nipy.load_image(os.path.join(image_path, im ))._data
            for k in data_4d:
                data_4d[k].append(images_data[region_coodinates[k]])
        except:
            raise ValueError("Error during reading image {}".format(str(im)))

    for c in region_codes:
            c=int(c)
            np_4d=np.array(data_4d[c])
            print np_4d.shape
            np.save(os.path.join(path_4d, str(c) +"_" + str(1)) ,  np_4d )
            convert_array_for_regression(path_4d, c)
            delete_arrays(path_4d, c)


def save_4d_data_region(logs_dir, atlas, image_path, path_4d, region_code, regexp='NO'):

    image_names=get_images_list(image_path,regexp)

    df=pd.DataFrame(image_names)
    df.to_csv(os.path.join(logs_dir, str(region_code)+ '.csv'))

    if len(image_names)<1000:
        if int(region_code)!=0:
            print 'FORCE MULTI JOBS SUBMISSION ( NOT EFFICIENT)'
        elif int(region_code)==0:
            save_4d_data(atlas, image_path, path_4d, image_names)

            return 0

    data_4d=[]
    part=1
    coordinate=np.where(atlas._data==int(region_code) )
    if coordinate[0].shape[0]==0:
        raise ValueError('Region code {} does not exist'.format(region_code))
    count=0
    for im in image_names:
    # reading all images and dump nparrays by voxels in region by 1000 images
            try:
                images_data=nipy.load_image(os.path.join(image_path, im ))._data
                count+=1
                data=images_data[coordinate]
                data_4d.append(data)

                if count==1000:
                    np_4d=np.array(data_4d)
                    np.save(os.path.join(path_4d, str(region_code) + "_" + str(part)) ,  np_4d )
                    data_4d=[]
                    np_4d=None
                    part+=1
                    count=0
            except:
                print ("Error during reading image {}".format(str(im)))

    if count!=0:
        np_4d=np.array(data_4d)
        np.save(os.path.join(path_4d, str(region_code) +"_" + str(part)) ,  np_4d )

    convert_array_for_regression(path_4d, region_code)

    delete_arrays(path_4d, region_code)


def experiment_save_4d(logs_dir, atlas_path,image_path, path_4d, region_code , reg):
    atlas=nipy.load_image(atlas_path)
    save_4d_data_region(logs_dir, atlas, image_path, path_4d, region_code , regexp=reg)





if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Convert nifti images to nparray files')
    parser.add_argument("-o",required=True, type=str, help="path to save result folder")
    parser.add_argument("-i",required=True, type=str, help="path to nifti images")
    parser.add_argument("-atlas",required=True, type=str, help="path to Atlas images to use to define voxel chunks")
    parser.add_argument("-code",required=True,type=int, help="Atlas chunk code")
    parser.add_argument("-regexp",type=str,default='NO', help="REGEXP to select images")
    parser.add_argument("-logs",type=str,required=True, help="path to save logs")

    args = parser.parse_args()
    print args
    with Timer() as t:
       experiment_save_4d(args.logs, args.atlas, args.i, args.o, args.code, args.regexp)
    print "save data for analysis %s s" %(t.secs)





