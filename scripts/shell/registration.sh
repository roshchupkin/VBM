#!/usr/bin/env bash
############################################
#
#
# REGISTRATION

DATA_PATH=${VBM_EXPERIMENT_DIR}/MRI

IMAGE_LIST=$( ls ${DATA_PATH} )


/bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_reg.sh

for filename in ${IMAGE_LIST[@]}; do


	f=${filename%.nii.gz*}


	echo "${FSLDIR}/bin/fsl_reg ${DATA_PATH}/${filename} ${TEMPLATE} \
	${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM \
	-fnirt \"--config=${FSL_CONFIG} --jout=${VBM_EXPERIMENT_DIR}/transformed/${f}_JAC_nl\" " >> ${VBM_EXPERIMENT_DIR}/fsl_reg.sh
	
done

chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_reg.sh


