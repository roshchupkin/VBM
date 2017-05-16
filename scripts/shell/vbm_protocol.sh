

############################################
#
#
#
#
# Rotterdam BIGR VBM Protocol
#
#
#
#
#
#
############################################
#
#
# READING CONFIGURATION FILE

sh ./config.sh


############################################
#
#
#  TISUE SEGMENTATION 

# skip this step if you already have you GM or (GM+WM) images
sh ${VBMDIR}/scripts/shell/tissue.sh 


############################################
#
#
# TEMPLATE CREATION

# You have to define pathway to TEMPLATE in configuration file. 
# If you don't have you own template you can use MNI template from ${VBMDIR}/standards/templates/
# Script to create template will be included in pipeline in next release.  

############################################
#
#
# REGISTRATION

sh ${VBMDIR}/scripts/shell/registration.sh 

############################################
#
#
# MODULATION


sh ${VBMDIR}/scripts/shell/modulation.sh 

############################################
#
#
# SMOOTHING

sh ${VBMDIR}/scripts/shell/smoothing.sh

############################################
#
#
# DATA CONVERTING

sh ${VBMDIR}/scripts/shell/converter.sh

############################################
#
#
# QC REGISTRATION 

sh ${VBMDIR}/scripts/shell/QC.sh

############################################
