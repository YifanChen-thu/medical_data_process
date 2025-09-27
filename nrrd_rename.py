import os

# 修改这里为你的 TCGA-OV 数据集的根目录
root_dir = r"/path/to/TCGA-OV/CT"

for case_name in os.listdir(root_dir):                       # 每个病例文件夹
    case_path = os.path.join(root_dir, case_name)
    if not os.path.isdir(case_path):
        continue

    for period_name in os.listdir(case_path):                # 每个时期文件夹
        period_path = os.path.join(case_path, period_name)
        if not os.path.isdir(period_path):
            continue

        # 找到该时期文件夹中的 _CT.nii 文件
        ct_files = [f for f in os.listdir(period_path) if f.endswith("_CT.nii")]
        if not ct_files:
            print(f"⚠️ 没有找到 _CT.nii 文件: {period_path}")
            continue
        if len(ct_files) > 1:
            print(f"⚠️ 发现多个 _CT.nii 文件: {period_path}")
            continue

        ct_file = ct_files[0]
        base_name = ct_file[:-7]  # 去掉 '_CT.nii'

        # 找到所有 .seg.nrrd 文件并改名
        for f in os.listdir(period_path):
            if f.endswith(".seg.nrrd"):
                old_path = os.path.join(period_path, f)
                new_name = f"{base_name}.seg.nrrd"
                new_path = os.path.join(period_path, new_name)

                # 如果新名字和旧名字不同就重命名
                if f != new_name:
                    os.rename(old_path, new_path)
                    print(f"✅ {old_path}  →  {new_path}")
                else:
                    print(f"➡️ 已是正确名字：{old_path}")