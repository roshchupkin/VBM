############################################
#
#
# SMOOTHING


MODULATION_FLAG=$1


 /bin/rm -f ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh

if [ $MODULATION_FLAG -eq 1]; then

	add=_GM_to_template_GM_mod
else
	add=_GM_to_template_GM
fi


for filename in ${IMAGE_LIST[@]}; do

	f=${filename%.nii.gz*}

	echo "${FSLDIR}/bin/fslmaths ${VBM_EXPERIMENT_DIR}/transformed/${f}${add} -s ${SMOOTH_KERNEL} ${VBM_EXPERIMENT_DIR}/smoothed/${f}${add}_s${SMOOTH_KERNEL}" >> ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh
done

chmod a+x ${VBM_EXPERIMENT_DIR}/fsl_smooth.sh

 
