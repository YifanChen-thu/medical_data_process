import os
import shutil

# 原始文件夹根路径
source_root = '/date/yifanchen/data_mask'
source_folders = [
    'Adrenal_CT_train_val_test',
    'Bladder_Kidney_CT_train_val_test',
    'Lung_CT_train_val_test',
    'Stomach_Colon_Liver_Pancreas_CT_train_val_test',
    'Uterus_Ovary_CT_train_val_test'
]

# 目标文件夹
target_root = '/date/yifanchen/data_mask/all_ct_mask_nii'

# train / val / test 三个子目录
splits = ['train', 'val', 'test']

for split in splits:
    # 在目标文件夹下创建 train/val/test 目录
    split_target_dir = os.path.join(target_root, split)
    os.makedirs(split_target_dir, exist_ok=True)

    for folder in source_folders:
        split_source_dir = os.path.join(source_root, folder, split)
        if not os.path.exists(split_source_dir):
            print(f"⚠️ 跳过 {split_source_dir}，不存在")
            continue

        # 遍历源 split 下的所有子文件夹
        for item in os.listdir(split_source_dir):
            s_path = os.path.join(split_source_dir, item)
            t_path = os.path.join(split_target_dir, item)

            if os.path.isdir(s_path):
                # 如果是目录，用 copytree 合并（存在则合并文件进去）
                if os.path.exists(t_path):
                    # 已存在 -> 逐文件复制
                    for root, _, files in os.walk(s_path):
                        rel_path = os.path.relpath(root, s_path)
                        target_subdir = os.path.join(t_path, rel_path)
                        os.makedirs(target_subdir, exist_ok=True)
                        for f in files:
                            shutil.copy2(os.path.join(root, f),
                                         os.path.join(target_subdir, f))
                else:
                    shutil.copytree(s_path, t_path)
            else:
                # 如果是文件，直接复制
                shutil.copy2(s_path, t_path)

print("✅ 所有数据已合并到", target_root)