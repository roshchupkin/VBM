#!/usr/bin/env bash
############################################
#
#
#  TISUE SEGMENTATION 


SEGMENTED_PATH=${VBM_EXPERIMENT_DIR}/original/

GM_FLAG=$2
GM_CODE=$3

if [ GM_FLAG -eq 1 ]; then

	TS_SCRIPT="tissue_segmentation.py"

	/bin/rm -f ${VBM_EXPERIMENT_DIR}/tissue_segmentation.sh

	IMAGE_LIST=$( ls $SEGMENTED_PATH )

	for im in ${IMAGE_LIST[@]}; do #TODO change script settings for new python segmentation script

		echo "python ${VBMDIR}/scripts/tools/${TS_SCRIPT} ${SEGMENTED_PATH}/${im} \
		${VBM_EXPERIMENT_DIR}/MRI/ ${GM_CODE}">> ${VBM_EXPERIMENT_DIR}/tissue_segmentation.sh
	done

	chmod a+x ${VBM_EXPERIMENT_DIR}/python_tissue.sh


	else 
		

	/bin/rm -f ${VBM_EXPERIMENT_DIR}/tissue_segmentation.sh

	IMAGE_LIST=$( ls ${VBM_EXPERIMENT_DIR}/original/ )

	for im in ${IMAGE_LIST[@]}; do

		echo "${FSLDIR}/bin/bet ${ORIGIN_PATH}/${im} ${VBM_EXPERIMENT_DIR}/MRI/brain_${im} -f 0.4 \
		${FSLDIR}/bin/fast -R 0.3 -H 0.1 -n 2 ${VBM_EXPERIMENT_DIR}/MRI/brain_${im} \
		${FSLDIR}/bin/immv ${VBM_EXPERIMENT_DIR}/GM/brain_${im}_pve_1 GM_${im} \
		/bin/rm -f ${VBM_EXPERIMENT_DIR}/MRI/brain_${im}" >> ${VBM_EXPERIMENT_DIR}/tissue_segmentation.sh

	done 
	chmod a+x ${VBM_EXPERIMENT_DIR}/tissue_segmentation.sh



fi
