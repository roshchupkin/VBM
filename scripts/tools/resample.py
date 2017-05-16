import sys
sys.path.append('/scratch/groshchupkin/python_scripts/myenv/lib/python2.7/site-packages/')
import numpy as np
import nibabel
from nilearn import image
import argparse
import os

def resample(input, ref, output):
    image_to_resample = nibabel.load(input)
    image2=nibabel.load(ref)
    resampled_image =image.resample_img(image_to_resample,target_affine = image2.get_affine(),
                                        interpolation="nearest",
                                        target_shape=image2.shape)
    nibabel.save(resampled_image,output)


parser = argparse.ArgumentParser(description='Script to resample nifti image from 1mm FSL MNI to 1mm RS MNI space')

parser.add_argument("-i",required=True ,type=str, help="input image")
parser.add_argument("-o",required=True ,type=str, help="output image")
parser.add_argument("-r",required=True, type=str, help="path to reference")

args = parser.parse_args()

print args
resample(args.i, args.r, args.o)