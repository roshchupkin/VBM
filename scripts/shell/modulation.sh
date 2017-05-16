############################################
#
#
# MODULATION


/bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_mod.sh

DATA_PATH=${VBM_EXPERIMENT_DIR}/GM/

IMAGE_LIST=$( ls ${GM_PATH} )


for filename in ${IMAGE_LIST[@]}; do

	f=${filename%.nii.gz*}	

	echo "${FSLDIR}/bin/fslmaths ${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM -mul ${VBM_EXPERIMENT_DIR}/transformed/${f}_JAC_nl ${VBM_EXPERIMENT_DIR}/transformed/${f}_GM_to_template_GM_mod -odt float" >> ${VBM_EXPERIMENT_DIR}/fsl_mod.sh
done
chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_mod.sh
