

REG_SCRIPT=/scratch/groshchupkin/RotterdamStudy/packages/vbm_dev/scripts/shell/regression.sh
MAP_SCRIPT=/scratch/groshchupkin/RotterdamStudy/packages/vbm_dev/scripts/tools/create_map.sh
SUM_SCRIPT=/scratch/groshchupkin/RotterdamStudy/packages/vbm_dev/scripts/tools/summary.py

TESTPATH=/scratch/groshchupkin/RotterdamStudy/packages/vbm_dev/tests/

rm -r ${TESTPATH}/maps/*
rm -r ${TESTPATH}/summary/*
rm -r ${TESTPATH}/regression/*
rm -r ${TESTPATH}/logs/*

rm ${TESTPATH}/maps.sh
rm ${TESTPATH}/sum.sh

for i in GM WM FA MD FLAIR; do
#for i in MD; do
sh ${REG_SCRIPT} -r "Age sex" \
-o ${TESTPATH}/regression/ \
-t ${TESTPATH}/data_frames/age_sex.csv -d ${i} -e ${i}

id1=`bigrsub -q day -R 4G -N test_${i} -t ${TESTPATH}/regression/${i}/python_regression_${i}.sh -l ${TESTPATH}/logs/`


for j in p_values p_values_inv t_stat b_values p_log se; do
echo "sh ${MAP_SCRIPT} -r ${TESTPATH}/regression/${i}/results/ -o ${TESTPATH}/maps/ -t ${j} -i 1 -n ${i}_${j}.nii.gz -d ${i}" >> ${TESTPATH}/maps.sh
done
echo "python ${SUM_SCRIPT} -p ${TESTPATH}/maps/${i}_p_values.nii.gz -t ${TESTPATH}/maps/${i}_b_values.nii.gz -o ${TESTPATH}/summary/ -n ${i}_Hammer.csv -th 0.01 -a Hammer" >> ${TESTPATH}/sum.sh
echo "python ${SUM_SCRIPT} -p ${TESTPATH}/maps/${i}_p_values.nii.gz -t ${TESTPATH}/maps/${i}_b_values.nii.gz -o ${TESTPATH}/summary/ -n ${i}_FreeSurfer.csv -th 0.01 -a FreeSurfer" >>${TESTPATH}/sum.sh
done
id2=`bigrsub -q day -R 2G -N test_map -j ${id1} -t ${TESTPATH}/maps.sh -l ${TESTPATH}/logs/`
bigrsub -q day -R 2G -N test_sum -j ${id2} -t ${TESTPATH}/sum.sh -l ${TESTPATH}/logs/

