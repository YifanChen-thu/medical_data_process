import os
import shutil
# 原始文件夹路径
source_root = '/date/yifanchen/data_no_mask/2D_jpg'
source_folders = [
    'Adrenal_one2one_jpg',
    'Bladder_one2one_jpg',
    'Lung_one2one_jpg',
    'Stomach_one2one_jpg',
    'Uterus_one2one_jpg'
]
source_folder='slice_split'
# 目标合并文件夹
target_root = '/date/yifanchen/data_no_mask/2D_jpg/allCT_split_slice_jpg'

# # 原始文件夹路径
# source_root = '/date/yifanchen/data_no_mask/2D_jpg'
# source_folders = [
#     'Adrenal_one2one_jpg',
#     'Bladder_one2one_jpg',
#     'Lung_one2one_jpg',
#     'Stomach_one2one_jpg',
#     'Uterus_one2one_jpg'
# ]
# source_folder='CT_CTC'
# # 目标合并文件夹
# target_root = '/date/yifanchen/data_no_mask/2D_jpg/all_CT2CTC_jpg'

# 保证目标文件夹存在
os.makedirs(target_root, exist_ok=True)

# train/val/test 子文件夹
splits = ['train', 'val', 'test']

for split in splits:
    # 创建目标 split 文件夹
    target_split_dir = os.path.join(target_root, split)
    os.makedirs(target_split_dir, exist_ok=True)

    # 遍历每个源文件夹
    for folder in source_folders:
        source_split_dir = os.path.join(source_root, folder, source_folder, split)
        if not os.path.exists(source_split_dir):
            print(f"Warning: {source_split_dir} does not exist, skipping.")
            continue

        # 遍历该 split 下的所有文件
        for filename in os.listdir(source_split_dir):
            source_file = os.path.join(source_split_dir, filename)
            target_file = os.path.join(target_split_dir, filename)

            # 避免重名，如果有重复文件名可加前缀
            if os.path.exists(target_file):
                name, ext = os.path.splitext(filename)
                target_file = os.path.join(target_split_dir, f"{folder}_{name}{ext}")

            # 拷贝文件到目标文件夹
            shutil.copy2(source_file, target_file)

print("合并完成！")