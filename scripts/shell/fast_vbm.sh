#!/usr/bin/env bash



# THIS SCRIPT CREATE THREE JOB FILES WHICH YOU CAN SUBMIT IN PARALLEL ON CLUSTER


# full pathway to GM images
DATA_PATH=

# full pathway to template image
TEMPLATE=

# full pathway to FSL config file (you need to change ref_mask parameter!)
FSL_CONFIG=

# full pathway where you want to save results
VBM_EXPERIMENT_DIR=

# size of kernel 
SMOOTH_KERNEL=

 
 

mkdir -p ${VBM_EXPERIMENT_DIR}/smoothed
mkdir -p ${VBM_EXPERIMENT_DIR}/transformed
 



############################################
#
#
# REGISTRATION



IMAGE_LIST=$( ls ${DATA_PATH} )


/bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_reg.sh

for filename in ${IMAGE_LIST[@]}; do


	f=${filename%.nii.gz*}


	echo "${FSLDIR}/bin/fsl_reg ${DATA_PATH}/${filename} ${TEMPLATE} \
	${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM \
	-fnirt \"--config=${FSL_CONFIG} --jout=${VBM_EXPERIMENT_DIR}/transformed/${f}_JAC_nl\" " >> ${VBM_EXPERIMENT_DIR}/fsl_reg.sh
	
done

chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_reg.sh


############################################
#
#
# MODULATION

/bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_mod.sh


for filename in ${IMAGE_LIST[@]}; do

	f=${filename%.nii.gz*}	

	echo "${FSLDIR}/bin/fslmaths ${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM -mul \
	${VBM_EXPERIMENT_DIR}/transformed/${f}_JAC_nl ${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM_mod -odt float" >> ${VBM_EXPERIMENT_DIR}/fsl_mod.sh
done
chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_mod.sh




############################################
#
#
# SMOOTHING

/bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh



for filename in ${IMAGE_LIST[@]}; do

	f=${filename%.nii.gz*}

	echo "${FSLDIR}/bin/fslmaths ${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM_mod -s ${SMOOTH_KERNEL} \
	${VBM_EXPERIMENT_DIR}/smoothed/${f}_GM_to_template_GM_mod_s${SMOOTH_KERNEL}" >> ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh
done

chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh

 
