#!/usr/bin/env bash

module load elastix

WORK_DIR=$1
TEMPLATE=$2
TEMPLATE_MASK=$3
IMAGE_T1=$4
IMAGE_SEG=$5
IMAGE=$6
ID=$7


DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p ${WORK_DIR}/${ID}

python ${DIR}/tissue_segmentation.py \
        -o ${WORK_DIR}/${ID} \
        -i ${IMAGE_T1} \
        -s ${IMAGE_SEG} \
        -type brain \
        -m y

python ${DIR}/tissue_segmentation.py \
        -o ${WORK_DIR}/${ID} \
        -i ${IMAGE_T1} \
        -s ${IMAGE_SEG} \
        -type brain \
        -m n



elastix  \
        -f ${TEMPLATE} \
        -m ${WORK_DIR}/${ID}/brain_${IMAGE_T1##*/}\
        -fMask ${TEMPLATE_MASK} \
        -mMask ${WORK_DIR}/${ID}/mask_brain_${IMAGE_T1##*/}\
        -p ${WORK_DIR}/elastix_affine.txt -p ${WORK_DIR}/elastix_bspline.txt \
        -out ${WORK_DIR}/${ID}


sform=`fslorient -getsform ${WORK_DIR}/${ID}/brain_${IMAGE_T1##*/}`
qform=`fslorient -getqform ${WORK_DIR}/${ID}/brain_${IMAGE_T1##*/}`

cp ${IMAGE} ${WORK_DIR}/${ID}

X=x
Y=y
Z=z

T1=${WORK_DIR}/${ID}/brain_${IMAGE_T1##*/}
I=${WORK_DIR}/${ID}/${IMAGE##*/}

echo $T1
echo $I

diff <(fslhd ${T1}) <(fslhd ${I}) | grep -q Right-to-Left
if [ $? -eq 0 ]; then
    X=-x
fi
diff <(fslhd $T1 ) <(fslhd $I) | grep -q Anterior-to-Posterior
if [ $? -eq 0 ]; then
    Y=-y
fi
diff <(fslhd $T1 ) <(fslhd $I) | grep -q Inferior-to-Superior
if [ $? -eq 0 ]; then
    Z=-z
fi

echo $X $Y $Z

#fslswapdim ${WORK_DIR}/${ID}/${IMAGE##*/} $X $Y $Z ${WORK_DIR}/${ID}/swap_${IMAGE##*/}
#fslorient -setsform ${sform} ${WORK_DIR}/${ID}/swap_${IMAGE##*/}
#fslorient -setqform ${qform} ${WORK_DIR}/${ID}/swap_${IMAGE##*/}
#fslorient -forceradiological ${WORK_DIR}/${ID}/swap_${IMAGE##*/}


#python ${DIR}/tissue_segmentation.py \
#        -o ${WORK_DIR}/${ID} \
#        -i ${WORK_DIR}/${ID}/swap_${IMAGE##*/} \
#        -s ${IMAGE_SEG} \
#        -type brain \
#        -m n

mkdir -p ${WORK_DIR}/${ID}/trans/

sed -i '/(FinalBSplineInterpolationOrder 3)/c\(FinalBSplineInterpolationOrder 0)' ${WORK_DIR}/${ID}/TransformParameters.1.txt

transformix -in ${WORK_DIR}/${ID}/${IMAGE##*/} \
            -tp ${WORK_DIR}/${ID}/TransformParameters.1.txt \
            -out ${WORK_DIR}/${ID}/trans/


rm ${WORK_DIR}/${ID}/brain_${IMAGE_T1##*/}
rm ${WORK_DIR}/${ID}/mask_brain_${IMAGE_T1##*/}
rm ${WORK_DIR}/${ID}/${IMAGE##*/}
#rm ${WORK_DIR}/${ID}/swap_${IMAGE##*/}
#rm ${WORK_DIR}/${ID}/brain_swap_${IMAGE##*/}
rm ${WORK_DIR}/${ID}/result.0.nii
rm ${WORK_DIR}/${ID}/result.1.nii
N=${IMAGE##*/}
N=${N%.gz*}
mv ${WORK_DIR}/${ID}/trans/result.nii ${WORK_DIR}/${ID}/MNI_${N}