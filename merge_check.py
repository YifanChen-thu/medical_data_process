import os

def check_merged_dataset(reference_dataset, merged_dataset):
    """
    检查合并后的数据集是否满足：
    1. 每个病例/时期下有且仅有3个文件，且为 _CT.nii / _CTC.nii / .nrrd
    2. 能与参考数据集的病例/时期结构一一对应
    """

    problems = []   # 存放所有问题
    ok = True

    # -------- 1️⃣ 内容完整性检查 --------
    print("=== 检查输出数据集内容 ===")
    for subset in ["train", "val", "test"]:
        merged_subset = os.path.join(merged_dataset, subset)
        if not os.path.isdir(merged_subset):
            problems.append(f"❌ 输出数据集缺少 {subset} 文件夹")
            ok = False
            continue

        for case in sorted(os.listdir(merged_subset)):
            case_path = os.path.join(merged_subset, case)
            if not os.path.isdir(case_path):
                continue
            for period in sorted(os.listdir(case_path)):
                period_path = os.path.join(case_path, period)
                if not os.path.isdir(period_path):
                    continue

                files = os.listdir(period_path)
                if len(files) != 3:
                    problems.append(f"[{subset}/{case}/{period}] 文件数不是3个，而是 {len(files)}")
                    ok = False
                    continue

                required_exts = {"_CT.nii", "_CTC.nii", ".nrrd"}
                exts_found = set()
                for f in files:
                    if f.endswith("_CT.nii"):
                        exts_found.add("_CT.nii")
                    elif f.endswith("_CTC.nii"):
                        exts_found.add("_CTC.nii")
                    elif f.endswith(".nrrd"):  # 包括 .seg.nrrd
                        exts_found.add(".nrrd")
                    else:
                        problems.append(f"[{subset}/{case}/{period}] 存在无效文件: {f}")
                        ok = False
                if exts_found != required_exts:
                    problems.append(f"[{subset}/{case}/{period}] 文件后缀不完整: {exts_found}")
                    ok = False

    # -------- 2️⃣ 结构对应检查 --------
    print("=== 检查与参考数据集结构对应 ===")
    for subset in ["train", "val", "test"]:
        ref_subset = os.path.join(reference_dataset, subset)
        merged_subset = os.path.join(merged_dataset, subset)

        if not os.path.isdir(ref_subset):
            problems.append(f"⚠️ 参考数据集缺少 {subset} 文件夹：{ref_subset}")
            continue

        for case in sorted(os.listdir(ref_subset)):
            ref_case_path = os.path.join(ref_subset, case)
            if not os.path.isdir(ref_case_path):
                continue
            for period in sorted(os.listdir(ref_case_path)):
                ref_period_path = os.path.join(ref_case_path, period)
                if not os.path.isdir(ref_period_path):
                    continue

                # 检查对应病例/时期是否存在于合并数据集中
                merged_period_path = os.path.join(merged_subset, case, period)
                if not os.path.isdir(merged_period_path):
                    problems.append(f"[{subset}/{case}/{period}] 在输出数据集中缺失")
                    ok = False

    # -------- 结果输出 --------
    if problems:
        print("\n❗发现以下问题：")
        for p in problems:
            print(" -", p)
    else:
        print("\n✅ 检查通过：所有文件和目录结构完全符合要求")

    return ok


# ===== 示例调用 =====
if __name__ == "__main__":
    reference = "/date/yifanchen/data/Uterus_Ovary_CT_train_val_test"
    merged   = "/date/yifanchen/data_mask/Uterus_Ovary_CT_train_val_test"
    check_merged_dataset(reference, merged)