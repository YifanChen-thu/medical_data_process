# a='Adrenal_Ki67_Seg_019_2007-12-22_CT.nii'
# modality='CT'
# print(a.split(modality)[0])
import os

root_dir = "../../data/Stomach_Colon_Liver_Pancreas_CT_train_val_test"

for dirpath, dirnames, filenames in os.walk(root_dir):
    # 遍历目录名
    for dirname in dirnames:
        if "术后" in dirname:
            print("目录:", os.path.join(dirpath, dirname))
    # 遍历文件名
    for filename in filenames:
        if "术后" in filename:
            print("文件:", os.path.join(dirpath, filename))