#!/usr/bin/env bash

DATA_TYPE="GM"

while getopts ":r:e:o:t:d:" opt; do
  case $opt in
    r) REGRESSION=$OPTARG ;;
    e) EXPERIMENT_NAME=$OPTARG ;;
    o) WORK_DIR=$OPTARG;;
    t) TABLE_PATH=$OPTARG;;
    d) DATA_TYPE=$OPTARG;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$REGRESSION" ]; then
	echo 'need -r regression model (columns in table, e.g. -r "sex age APOE") '
	exit 2
fi
if [ -z "$EXPERIMENT_NAME"  ]; then
	echo "need -e experiment name"
	exit 2
fi
if [ -z "$WORK_DIR" ]; then
	echo "need -o output folder"
	exit 2
fi
if [ -z "$TABLE_PATH" ]; then
	echo "need -t data table"
	exit 2
fi
if [ -z "$DATA_TYPE" ]; then
	echo "need -d data type: FA, GM, WM, FLAIR, MD, CON_DEN,CON_MAX. Example, -d FA"
	exit 2
fi

echo "Data type: ${DATA_TYPE}"
echo "regression: ${REGRESSION}"
echo "Experiment name: ${EXPERIMENT_NAME}"
echo "Working dir: ${WORK_DIR}"
echo "Table path: ${TABLE_PATH}"


PYTHON_SCRIPT_PATH='/scratch/groshchupkin/RotterdamStudy/packages/vbm/scripts/python/'
SCRIPT_NAME='epi_regression.py'

if [ $DATA_TYPE == "GM" ]; then
    DATA_PATH='/scratch/groshchupkin/RotterdamStudy/VBM/GM/nparray_RS/'
elif [ $DATA_TYPE == "FA" ]; then
    DATA_PATH='/archive/groshchupkin/Rotterdam_DTI/nparray_RS/'
elif [ $DATA_TYPE == "WM" ]; then
    DATA_PATH='/scratch/groshchupkin/RotterdamStudy/VBM/WM/nparray_RS/'
elif [ $DATA_TYPE == "FLAIR" ]; then
    DATA_PATH='/scratch/groshchupkin/RotterdamStudy/VBM/FLAIR/nparray_RS/'
elif [ $DATA_TYPE == "MD" ]; then
    DATA_PATH='/scratch/groshchupkin/RotterdamStudy/DTI/MD/nparray_RS/'
elif [ $DATA_TYPE == "CON_DEN" ]; then
    DATA_PATH='/scratch/groshchupkin/Connectome/voxels/affectednessMap_density/nparray_RS/'
elif [ $DATA_TYPE == "CON_MAX" ]; then
    DATA_PATH='/scratch/groshchupkin/Connectome/voxels/affectednessMap_maxVox/nparray_RS/'
else
    echo "${DATA_TYPE} not available!"
    exit 2
fi
echo "Data path: ${DATA_PATH}"

SAVE_RESULT_DIR=${WORK_DIR}${EXPERIMENT_NAME}/results/

ROI_ARRAY=`for i in $(ls ${DATA_PATH} | grep reg );do c=${i%.npy};c=${c:3}; echo $c; done | awk 'BEGIN {FS="_"}{print $1}' | sort -n | uniq`



cd ${WORK_DIR}

mkdir -p ${EXPERIMENT_NAME}

mkdir -p ${SAVE_RESULT_DIR}

cd ${EXPERIMENT_NAME}

rm -f ${WORK_DIR}${EXPERIMENT_NAME}/python_regression_${EXPERIMENT_NAME}.sh


for ROI in ${ROI_ARRAY[@]}; do

	echo "python ${PYTHON_SCRIPT_PATH}${SCRIPT_NAME} -roi ${ROI} -o ${SAVE_RESULT_DIR} -r ${REGRESSION} -d ${DATA_PATH} -t ${TABLE_PATH} -type ${DATA_TYPE} ">> ${WORK_DIR}${EXPERIMENT_NAME}/python_regression_${EXPERIMENT_NAME}.sh

	chmod a+x ${WORK_DIR}${EXPERIMENT_NAME}/python_regression_${EXPERIMENT_NAME}.sh
done

echo "
There is bash script in ${WORK_DIR}${EXPERIMENT_NAME},
you can run it on cluster, each line is separate job,
or just in shell, but it will take more time!
"