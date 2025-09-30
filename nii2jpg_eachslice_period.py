import os
import nibabel as nib
import imageio
import numpy as np

def normalize_slice(slice_2d):
    """归一化到 0-255"""
    slice_norm = (slice_2d - slice_2d.min()) / (slice_2d.ptp() + 1e-8)
    return (slice_norm * 255).astype(np.uint8)

def convert_period(period_path, output_period_path, axis=2):
    """处理单个 period 文件夹里的 nii 文件"""
    nii_files = sorted([f for f in os.listdir(period_path) if f.endswith(".nii") or f.endswith(".nii.gz")])
    if not nii_files:
        return  # period 下没有 nii 文件就跳过

    # 用第一个 nii 文件确定切片数
    ref_img = nib.load(os.path.join(period_path, nii_files[0]))
    ref_data = ref_img.get_fdata()
    num_slices = ref_data.shape[axis]

    for i in range(num_slices):
        slice_folder = os.path.join(output_period_path, f"slice{i+1:03d}")
        os.makedirs(slice_folder, exist_ok=True)

        for f in nii_files:
            nii_path = os.path.join(period_path, f)
            base_name = f.replace(".nii.gz", "").replace(".nii", "")

            img = nib.load(nii_path)
            data = img.get_fdata()

            if axis == 0:
                slice_2d = data[i, :, :]
            elif axis == 1:
                slice_2d = data[:, i, :]
            else:
                slice_2d = data[:, :, i]
            slice_2d = np.rot90(slice_2d, k=-1)#顺时针旋转
            slice_norm = normalize_slice(slice_2d)

            out_path = os.path.join(slice_folder, f"{base_name}.jpg")
            imageio.imwrite(out_path, slice_norm)

        print(f"{os.path.basename(period_path)}: slice {i+1}/{num_slices} done.")

def convert_patient(patient_path, output_patient_path, axis=2):
    """遍历 patient 下的 period 文件夹"""
    for period in os.listdir(patient_path):
        period_path = os.path.join(patient_path, period)
        if not os.path.isdir(period_path):
            continue  # 忽略非文件夹（如 .DS_Store）

        output_period_path = os.path.join(output_patient_path, period)
        os.makedirs(output_period_path, exist_ok=True)

        convert_period(period_path, output_period_path, axis=axis)

def nii_to_jpg_dataset(input_root, output_root, axis=2):
    """转换整个 train/val/test 数据集"""
    for split in ["train", "val", "test"]:
        split_input = os.path.join(input_root, split)
        split_output = os.path.join(output_root, split)

        if not os.path.exists(split_input):
            continue

        for patient in os.listdir(split_input):
            patient_path = os.path.join(split_input, patient)
            if not os.path.isdir(patient_path):
                continue  # 忽略非文件夹

            output_patient_path = os.path.join(split_output, patient)
            os.makedirs(output_patient_path, exist_ok=True)

            convert_patient(patient_path, output_patient_path, axis=axis)

if __name__ == "__main__":
    organs = ['Adrenal','Bladder_Kidney','Lung','Stomach_Colon_Liver_Pancreas','Uterus_Ovary']
    for organ in organs:
        input_root = f"../../data/{organ}_CT_train_val_test"
        output_root = f"/date/yifanchen/data_no_mask/2D_jpg/{organ.split('_')[0]}_one2one_jpg/slice_split"
        nii_to_jpg_dataset(input_root, output_root, axis=2)

"""
/date/yifanchen/data_no_mask/2D_jpg/Adrenal_one2one_jpg/slice_split/
/date/yifanchen/data_no_mask/2D_jpg/Bladder_one2one_jpg/slice_split/
/date/yifanchen/data_no_mask/2D_jpg/Lung_one2one_jpg/slice_split/
/date/yifanchen/data_no_mask/2D_jpg/Stomach_one2one_jpg/slice_split/
/date/yifanchen/data_no_mask/2D_jpg/Uterus_one2one_jpg/slice_split/
#ct
input:
../../data/Adrenal_CT_train_val_test/
├── train/
│   ├── TCGA-DK-A3WW/
│   │   ├── 07-07-1999-NA-FORFILE CT ABD ANDOR PEL - CD-13195/
│   │   │   ├── TCGA-DK-A3WW_1999-07-07_CT.nii
│   │   │   └── TCGA-DK-A3WW_1999-07-07_CTC.nii
│   │   └── 08-08-2000-ANOTHER-CT-FOLDER/
│   │       ├── TCGA-DK-A3WW_2000-08-08_CT.nii
│   │       └── TCGA-DK-A3WW_2000-08-08_CTC.nii
│   └── ...
├── val/
│   └── ...
└── test/
    └── ...

output:
/date/yifanchen/data_no_mask/2D_jpg/Adrenal_one2one_jpg/slice_split/
├── train/
│   ├── TCGA-DK-A3WW/
│   │   ├── 07-07-1999-NA-FORFILE CT ABD ANDOR PEL - CD-13195/
│   │   │   ├── slice001/
│   │   │   │   ├── TCGA-DK-A3WW_1999-07-07_CT.jpg
│   │   │   │   └── TCGA-DK-A3WW_1999-07-07_CTC.jpg
│   │   │   ├── slice002/
│   │   │   │   ├── TCGA-DK-A3WW_1999-07-07_CT.jpg
│   │   │   │   └── TCGA-DK-A3WW_1999-07-07_CTC.jpg
│   │   │   └── ...
│   │   └── 08-08-2000-ANOTHER-CT-FOLDER/
│   │       ├── slice001/
│   │       │   ├── TCGA-DK-A3WW_2000-08-08_CT.jpg
│   │       │   └── TCGA-DK-A3WW_2000-08-08_CTC.jpg
│   │       └── ...
│   └── ...
├── val/
│   └── ...
└── test/
    └── ...
"""