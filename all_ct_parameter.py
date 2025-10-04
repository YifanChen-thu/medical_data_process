import os
import numpy as np
import nibabel as nib
import nrrd
from pathlib import Path
import random

def analyze_dataset(root_dir, max_cases=50, sample_voxels=100000):
    """
    root_dir: 数据集根目录
    max_cases: 最多采样多少病例 (避免全量太慢)
    sample_voxels: 每个病例随机抽取的体素数
    """
    ctc_files = []
    seg_files = []

    for split in ["train", "val", "test"]:
        split_dir = Path(root_dir) / split
        for patient in split_dir.glob("*"):
            if not patient.is_dir():
                continue
            for period in patient.glob("*"):
                if not period.is_dir():
                    continue

                ctc = list(period.glob("*_CTC.nii")) + list(period.glob("*_CTC.nii.gz"))
                seg = list(period.glob("*.seg.nrrd")) + list(period.glob("*.nrrd"))

                if len(ctc) == 1 and len(seg) == 1:
                    ctc_files.append(ctc[0])
                    seg_files.append(seg[0])

    print(f"[INFO] 找到 {len(ctc_files)} 个 CTC, {len(seg_files)} 个 seg")

    if not ctc_files or not seg_files:
        print("[ERROR] 没有找到有效的CTC或seg文件")
        return

    # 随机抽样一部分病例
    random.shuffle(ctc_files)
    ctc_files = ctc_files[:max_cases]

    all_means, all_stds = [], []
    global_min, global_max = float("inf"), float("-inf")
    sample_shapes = []

    for f in ctc_files:
        img = nib.load(str(f))
        dataobj = img.dataobj  # 惰性访问，不转float64
        shape = img.shape
        sample_shapes.append(shape)

        # 随机采样部分体素
        num_vox = np.prod(shape)
        idx = np.random.choice(num_vox, size=min(sample_voxels, num_vox), replace=False)
        vals = np.asarray(dataobj).ravel()[idx]

        all_means.append(vals.mean())
        all_stds.append(vals.std())
        global_min = min(global_min, vals.min())
        global_max = max(global_max, vals.max())

    print("\n=== 图像统计 (CTC) ===")
    print("采样病例数:", len(ctc_files))
    print("intensity_range:", (global_min, global_max))
    print("global_mean:", np.mean(all_means))
    print("global_std:", np.mean(all_stds))
    print("sample_shapes (前5个):", sample_shapes[:5])

    # --- 分割标签统计 (只取部分病例避免太慢) ---
    random.shuffle(seg_files)
    seg_files = seg_files[:max_cases]

    all_labels = set()
    for f in seg_files:
        data, _ = nrrd.read(str(f))
        uniq = np.unique(data)
        all_labels.update(uniq.tolist())

    print("\n=== 分割标签统计 ===")
    print("采样病例数:", len(seg_files))
    print("所有出现的 label 值:", sorted(all_labels))
    if all_labels:
        print("推荐 target_class:", max(all_labels))


if __name__ == "__main__":
    root_dir = "/date/yifanchen/data_mask/all_ct_mask_nii"
    analyze_dataset(root_dir, max_cases=50, sample_voxels=100000)