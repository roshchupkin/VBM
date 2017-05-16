#!/bin/sh



NII2NP_SCRIPT="nii2np.py"

CONVERTED_DIR="${VBM_EXPERIMENT_DIR}/nparray/"


DATA_PATH="${VBM_EXPERIMENT_DIR}/smoothed/"

#ATLAS_IMAGE_PATH="${VBMDIR}/standards/atlases/Hammer_1mm_MNI.nii.gz"
# TODO check size of Atlas and images!

PYTHON_SCRIPT_PATH="${VBMDIR}/scripts/python/"

REGEXP="NO"

ROI_ARRAY=$(seq 1 83)

/bin/rm -f ${VBM_EXPERIMENT_DIR}/nii2py.sh


IMAGE_NUMBER=`ls ${DATA_PATH} | wc -l`

if [ $IMAGE_NUMBER -le 1000 ] && [ REGEXP!="NO" ]; then 


echo "It is not efficient split to multi jobs, let us run it at once..."

echo "python ${PYTHON_SCRIPT_PATH}${NII2NP_SCRIPT} ${VBM_EXPERIMENT_DIR} ${ATLAS_IMAGE_PATH} ${DATA_PATH} ${CONVERTED_DIR} 0 ${REGEXP}"> ${VBM_EXPERIMENT_DIR}/nii2py.sh

chmod a+x ${VBM_EXPERIMENT_DIR}/nii2py.sh


else	

	for ROI in ${ROI_ARRAY[@]}; do

		echo "python ${PYTHON_SCRIPT_PATH}${NII2NP_SCRIPT} ${VBM_EXPERIMENT_DIR} ${ATLAS_IMAGE_PATH} ${DATA_PATH} ${CONVERTED_DIR} ${ROI} ${REGEXP}">> ${VBM_EXPERIMENT_DIR}/nii2py.sh
	done
	chmod a+x ${VBM_EXPERIMENT_DIR}/nii2py.sh
fi



