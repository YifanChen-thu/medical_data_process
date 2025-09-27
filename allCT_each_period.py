import os
import shutil

source_root = '/date/yifanchen/data_no_mask/2D_jpg'
source_folders = [
    'Adrenal_one2one_jpg',
    'Bladder_one2one_jpg',
    'Lung_one2one_jpg',
    'Stomach_one2one_jpg',
    'Uterus_one2one_jpg'
]
source_folder = 'slice_split'

target_root = '/date/yifanchen/data_no_mask/2D_jpg/allCT_split_slice_jpg'
os.makedirs(target_root, exist_ok=True)

splits = ['train', 'val', 'test']

for split in splits:
    target_split_dir = os.path.join(target_root, split)
    os.makedirs(target_split_dir, exist_ok=True)

    for folder in source_folders:
        source_split_dir = os.path.join(source_root, folder, source_folder, split)
        if not os.path.exists(source_split_dir):
            print(f"Warning: {source_split_dir} does not exist, skipping.")
            continue

        # 遍历 patient 文件夹
        for patient in os.listdir(source_split_dir):
            patient_dir = os.path.join(source_split_dir, patient)
            if not os.path.isdir(patient_dir):
                continue

            # 复制整个 patient 目录到目标 split 下
            target_patient_dir = os.path.join(target_split_dir, patient)

            # 如果目标里已经存在同名 patient，可以改名避免冲突
            if os.path.exists(target_patient_dir):
                target_patient_dir = os.path.join(
                    target_split_dir, f"{folder}_{patient}"
                )

            shutil.copytree(patient_dir, target_patient_dir)

print("合并完成！")