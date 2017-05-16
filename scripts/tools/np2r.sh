
DATA_PATH=$1
DATA_SAVE=$2

NAME=`basename ${DATA_PATH}`
NAME=${NAME%.npy*}


python ${VBMDIR}/scripts/tools/np2bin.py ${DATA_PATH} ${DATA_SAVE}
Rscript ${VBMDIR}/scripts/tools/bin2r.r ${NAME} ${DATA_SAVE}

rm ${DATA_SAVE}/data${NAME}.bin