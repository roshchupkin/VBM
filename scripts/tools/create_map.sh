

DATA_TYPE="GM"

while getopts ":r:i:o:t:n:d:" opt; do
  case $opt in
    r) RESULT_PATH=$OPTARG ;;
    i) INDEX=$OPTARG ;;
    o) OUT_PATH=$OPTARG;;
    t) TYPE=$OPTARG;;
    n) SAVE_NAME=$OPTARG;;
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

if [ -z "$RESULT_PATH" ]; then
	echo "need -r Regession result folder"
	exit 2
fi
if [ -z "$OUT_PATH" ]; then
	echo "need -o Out folder"
	exit 2
fi
if [ -z "$TYPE" ]; then
	echo "need -t Map type ('p_values','p_values_inv','t_stat','b_values','p_log','se')"
	exit 2
fi
if [ -z "$INDEX" ]; then
	echo "need -i covariate index"
	exit 2
fi
if [ -z "$SAVE_NAME" ]; then
	echo "need -n save file name"
	exit 2
fi

echo "Data type: ${DATA_TYPE}"
echo "Regession result folder: ${RESULT_PATH}"
echo "Out folder: ${OUT_PATH}"
echo "Map type: ${TYPE}"
echo "Covariate index: ${INDEX}"
echo "Save map name: ${SAVE_NAME}"


RS_REFERENCE=/archive/groshchupkin/NeuroData/Templates/MNI/mni_icbm152_brain.nii.gz
SCRIPT_PATH=/scratch/groshchupkin/RotterdamStudy/packages/vbm/scripts/tools/
SCRIPT_NAME=create_map.py

if [ $DATA_TYPE == "GM" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/mni_icbm152_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_GM_mask_1mm_MNI_kNN_conservative.nii.gz
elif [ $DATA_TYPE == "WM" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/mni_icbm152_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_WM_mask_1mm_MNI_kNN.nii.gz
elif [ $DATA_TYPE == "FA" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/MNI152lin_T1_1mm_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz
elif [ $DATA_TYPE == "FLAIR" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/mni_icbm152_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_FLAIR_mask_1mm_MNI.nii.gz
elif [ $DATA_TYPE == "MD" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/MNI152lin_T1_1mm_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz
elif [ $DATA_TYPE == "CON_DEN" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/MNI152lin_T1_1mm_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz
elif [ $DATA_TYPE == "CON_MAX" ]; then
    TEMPLATE=/archive/groshchupkin/NeuroData/Templates/MNI/MNI152lin_T1_1mm_brain.nii.gz
    ATLAS=/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz
    MASK=/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz
else
    echo "Data type ${DATA_TYPE} not available!"
    exit 2
fi

python ${SCRIPT_PATH}${SCRIPT_NAME} -i ${RESULT_PATH} \
                                    -o ${OUT_PATH} \
                                    -t ${TEMPLATE} \
                                    -type ${TYPE} \
                                    -a ${ATLAS} \
                                    -index ${INDEX} \
                                    --name ${SAVE_NAME} \
                                    -mask ${MASK}


if [ $DATA_TYPE == "FA" ] || [ $DATA_TYPE == "MD" ] || [ $DATA_TYPE == "CON_DEN" ] || [ $DATA_TYPE == "CON_MAX" ]; then
    echo ${DATA_TYPE}
    if [ $TYPE == "t_stat" ]; then
        python ${SCRIPT_PATH}/resample.py -i ${OUT_PATH}/neg_${SAVE_NAME} -r ${RS_REFERENCE} -o ${OUT_PATH}/neg_${SAVE_NAME}
        python ${SCRIPT_PATH}/resample.py -i ${OUT_PATH}/pos_${SAVE_NAME} -r ${RS_REFERENCE} -o ${OUT_PATH}/pos_${SAVE_NAME}
    else
    python ${SCRIPT_PATH}/resample.py -i ${OUT_PATH}/${SAVE_NAME} -r ${RS_REFERENCE} -o ${OUT_PATH}/${SAVE_NAME}
    fi

fi