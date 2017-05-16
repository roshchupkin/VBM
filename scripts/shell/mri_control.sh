#!/bin/sh

#TODO check this script? delete?

SCRIPT_NAME="QC_vbm_reg.py"

DATA_PATH="${VBM_EXPERIMENT_DIR}/nparray/"

SAVE_PATH="${VBM_EXPERIMENT_DIR}/mri_control/"

REGION_CODE=$1

THRESHOLD=$2

python ${PYTHON_SCRIPT_PATH}${SCRIPT_NAME} ${DATA_PATH} ${REGION_CODE} ${SAVE_PATH} ${THRESHOLD}
