import os

VBMDIR=os.path.abspath(os.path.dirname(__file__))
os.environ['VBMDIR']=VBMDIR

INFO_TABLE={
	"GM":'/scratch/groshchupkin/RotterdamStudy/VBM/GM/data_frames/VBM_GM_mri_list.csv',
	"WM":'/scratch/groshchupkin/RotterdamStudy/VBM/WM/data_frames/VBM_WM_mri_list.csv',
	"FA":'/archive/groshchupkin/Rotterdam_DTI/data_frames/DTI_FA_mri_list.csv',
	"FLAIR":'/scratch/groshchupkin/RotterdamStudy/VBM/FLAIR/data_frames/VBM_FLAIR_mri_list.csv',
	"Hammer": '/archive/groshchupkin/NeuroData/Atlases/Hammer/Hammer_table.csv',
	"FreeSurfer" : '/archive/groshchupkin/NeuroData/Atlases/FreeSurfer/FreeSurfer_table.csv',
	"MD":'/scratch/groshchupkin/RotterdamStudy/DTI/MD/data_frames/VBM_MD_mri_list.csv',
	"CON_DEN":'/scratch/groshchupkin/Connectome/voxels/affectednessMap_density/data_frames/VBM_CON_density_mri_list.csv',
	"CON_MAX":'/scratch/groshchupkin/Connectome/voxels/affectednessMap_maxVox/data_frames/VBM_CON_maxVol_mri_list.csv',
	"Tracts":'/archive/groshchupkin/NeuroData/Atlases/Tracts_table_RS.csv'
			}


MASK={
	"GM":'/archive/groshchupkin/NeuroData/Masks/Brain_GM_mask_1mm_MNI_kNN_conservative.nii.gz',
	"WM":'/archive/groshchupkin/NeuroData/Masks/Brain_WM_mask_1mm_MNI_kNN.nii.gz',
	"FA":'/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz',
	"FLAIR":'/archive/groshchupkin/NeuroData/Masks/Brain_FLAIR_mask_1mm_MNI.nii.gz',
	"MD":'/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz',
	"CON_DEN":'/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz',
	"CON_MAX":'/archive/groshchupkin/NeuroData/Masks/Brain_FA_mask_1mm_MNI_kNN.nii.gz',
	"Tracts":'/archive/groshchupkin/NeuroData/Atlases/baseline_mni_tracts_09.nii.gz' #actually do not use!
	}

ATLAS={
	"GM":'/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz',
	"WM":'/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz',
	"FA":'/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz',
	"FLAIR":'/archive/groshchupkin/NeuroData/Atlases/brain_vbm_atlas.nii.gz',
	"Hammer":'/archive/groshchupkin/NeuroData/Atlases/Hammer/Hammer_1mm_MNI.nii.gz',
	"FreeSurfer":'/archive/groshchupkin/NeuroData/Atlases/FreeSurfer/FreeSurfer_1mm_fullseg.nii.gz',
	"MD":"/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz",
	"CON_DEN":'/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz',
	"CON_MAX":'/archive/groshchupkin/NeuroData/Atlases/brain_tbm_atlas.nii.gz',
	"Tracts": '/archive/groshchupkin/NeuroData/Atlases/baseline_th_rs_mni_tracts.nii.gz'
	}