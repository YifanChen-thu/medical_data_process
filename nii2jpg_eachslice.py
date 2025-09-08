import os
import nibabel as nib
import imageio
import numpy as np

def normalize_slice(slice_2d):
    """归一化到 0-255"""
    slice_norm = (slice_2d - slice_2d.min()) / (slice_2d.ptp() + 1e-8)
    return (slice_norm * 255).astype(np.uint8)

def convert_patient(patient_path, output_patient_path, axis=2):
    """处理单个病例文件夹"""
    nii_files = sorted([f for f in os.listdir(patient_path) if f.endswith(".nii") or f.endswith(".nii.gz")])
    if not nii_files:
        return

    # 用第一个模态确定切片数
    ref_img = nib.load(os.path.join(patient_path, nii_files[0]))
    ref_data = ref_img.get_fdata()
    num_slices = ref_data.shape[axis]

    for i in range(num_slices):
        slice_folder = os.path.join(output_patient_path, f"slice_{i+1:03d}")
        os.makedirs(slice_folder, exist_ok=True)

        for f in nii_files:
            nii_path = os.path.join(patient_path, f)
            base_name = f.replace(".nii.gz", "").replace(".nii", "")

            img = nib.load(nii_path)
            data = img.get_fdata()

            if axis == 0:
                slice_2d = data[i, :, :]
            elif axis == 1:
                slice_2d = data[:, i, :]
            else:
                slice_2d = data[:, :, i]
            slice_2d = np.rot90(slice_2d) #逆时针旋转 90°
            slice_norm = normalize_slice(slice_2d)

            out_path = os.path.join(slice_folder, f"{base_name}.jpg")
            imageio.imwrite(out_path, slice_norm)

        print(f"{os.path.basename(patient_path)}: slice {i+1}/{num_slices} done.")

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
                continue

            output_patient_path = os.path.join(split_output, patient)
            os.makedirs(output_patient_path, exist_ok=True)

            convert_patient(patient_path, output_patient_path, axis=axis)

if __name__ == "__main__":
    input_root = "/date/yifanchen/data_no_mask/Breast_MR_train_val_test_nii_dce_only"
    output_root = "/date/yifanchen/data_no_mask/2D_jpg/Breast_split_slice_jpg"
    nii_to_jpg_dataset(input_root, output_root, axis=2)

"""
#dce
input:
/date/yifanchen/data_no_mask/Breast_MR_train_val_test_nii_dce_only/
├── train/
│   ├── UCSF-BR-50/
│   │   ├── UCSF-BR-50_dce1.nii
│   │   ├── UCSF-BR-50_dce2.nii
│   │   └── UCSF-BR-50_dce3.nii
│   ├── UCSF-BR-51/
│   │   ├── UCSF-BR-51_dce1.nii
│   │   ├── UCSF-BR-51_dce2.nii
│   │   └── UCSF-BR-51_dce3.nii
│   └── ...
├── val/
│   └── (同 train 结构)
└── test/
    └── (同 train 结构)

output:
/date/yifanchen/data_no_mask/2D_jpg/Breast_split_slice_jpg/
├── train/
│   ├── UCSF-BR-50/
│   │   ├── slice_001/
│   │   │   ├── UCSF-BR-50_dce1.jpg
│   │   │   ├── UCSF-BR-50_dce2.jpg
│   │   │   └── UCSF-BR-50_dce3.jpg
│   │   ├── slice_002/
│   │   │   ├── UCSF-BR-50_dce1.jpg
│   │   │   ├── UCSF-BR-50_dce2.jpg
│   │   │   └── UCSF-BR-50_dce3.jpg
│   │   └── ...
│   ├── UCSF-BR-51/
│   │   ├── slice_001/
│   │   │   ├── UCSF-BR-51_dce1.jpg
│   │   │   ├── UCSF-BR-51_dce2.jpg
│   │   │   └── UCSF-BR-51_dce3.jpg
│   │   └── ...
│   └── ...
├── val/
│   └── (同 train 结构)
└── test/
    └── (同 train 结构)
"""