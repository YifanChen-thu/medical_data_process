import os
import pickle
import random
import numpy as np
from pathlib import Path

def collect_cases(root_dir, splits=("train", "val", "test")):
    """
    root_dir: 数据集根目录 (含 train/ val/ test)
    返回: {split: {case_id: [rel_img_path, rel_seg_path]}}
    """
    root_dir = Path(root_dir).resolve()
    all_cases = {s: {} for s in splits}

    for split in splits:
        split_dir = root_dir / split
        if not split_dir.exists():
            continue
        for patient_period in split_dir.glob("*/*"):  # 病例-时期
            if not patient_period.is_dir():
                continue

            patient_id = patient_period.parent.name
            period_id = patient_period.name
            case_id = f"{patient_id}_{period_id}"

            # 找 CTC 和 seg
            ctc_files = list(patient_period.glob("*_CTC.nii*"))
            seg_files = list(patient_period.glob("*.nrrd"))
            if not seg_files:
                seg_files = list(patient_period.glob("*label*.nii*")) + list(patient_period.glob("*.nii*"))

            if len(ctc_files) != 1 or len(seg_files) != 1:
                print(f"[WARN] {patient_period} 文件数量异常")
                print(f"  找到的 CTC: {ctc_files}")
                print(f"  找到的 SEG: {seg_files}")
                for f in patient_period.glob("*"):
                    print("   ->", f.name)
                continue

            # 存相对路径
            all_cases[split][case_id] = [
                str(ctc_files[0].relative_to(root_dir)),
                str(seg_files[0].relative_to(root_dir))
            ]

    return all_cases


def make_split_pkl(all_cases, output_path, num_folds=5, seed=42):
    """
    all_cases: {"train": {...}, "val": {...}, "test": {...}}
    输出: 5 折划分，每折都有 train/val/test
    """
    # train+val 作为交叉验证全集
    trainval_cases = {**all_cases["train"], **all_cases["val"]}
    test_cases = all_cases["test"]

    cases = list(trainval_cases.keys())
    random.seed(seed)
    random.shuffle(cases)

    folds = []
    fold_cases = np.array_split(cases, num_folds)

    for i in range(num_folds):
        val_cases = list(fold_cases[i])
        train_cases = [c for j, f in enumerate(fold_cases) if j != i for c in f]

        split_dict = {"train": {}, "val": {}, "test": {}}
        for c in train_cases:
            split_dict["train"][c] = trainval_cases[c]
        for c in val_cases:
            split_dict["val"][c] = trainval_cases[c]
        for c in test_cases.keys():
            split_dict["test"][c] = test_cases[c]

        folds.append(split_dict)

        print(f"[Fold {i}] train={len(train_cases)}, val={len(val_cases)}, test={len(test_cases)}")

    with open(output_path, "wb") as f:
        pickle.dump(folds, f)

    print(f"[INFO] 已保存 {output_path}, 5折, train+val={len(cases)}, test固定={len(test_cases)}")


if __name__ == "__main__":
    root_dir = "/date/yifanchen/data_mask/all_ct_mask_nii"   # 含 train/val/test
    output_pkl = os.path.join(root_dir, "split.pkl")

    all_cases = collect_cases(root_dir)
    total = sum(len(v) for v in all_cases.values())
    print(f"[INFO] 共收集 {total} 个病例 (train={len(all_cases['train'])}, "
          f"val={len(all_cases['val'])}, test={len(all_cases['test'])})")

    make_split_pkl(all_cases, output_pkl, num_folds=5)