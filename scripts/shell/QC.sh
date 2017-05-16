#!/usr/bin/env bash
############################################
#
#
# QC REGISTRATION 

Q_THRESHOLD=5

D_THRESHOLD=0.1

PYTHON_SCRIPT_PATH=${VBMDIR}/scripts/python/

QC_SCRIPT="QC_vbm_reg.py"

MRI_CONTROL_DIR=${VBM_EXPERIMENT_DIR}/mri_control/

ROI_ARRAY=$(seq 1 83)

/bin/rm -f ${VBM_EXPERIMENT_DIR}/vbm_qc.sh

for ROI in ${ROI_ARRAY[@]}; do

	echo "python ${PYTHON_SCRIPT_PATH}${QC_SCRIPT} ${CONVERTED_DIR} ${ROI} ${MRI_CONTROL_DIR} ${Q_THRESHOLD} ${D_THRESHOLD} ">> ${VBM_EXPERIMENT_DIR}/vbm_qc.sh		
done

chmod a+x ${VBM_EXPERIMENT_DIR}/vbm_qc.sh

