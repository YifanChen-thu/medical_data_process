import os
import shutil

def merge_datasets(reference_dataset, datasets_to_merge, output_root="/date/yifanchen/data_mask"):
    """
    根据参考数据集的结构，从多个待合并数据集中提取对应病例/时期的
    _CT.nii、_CTC.nii 和 .nrrd（含 .seg.nrrd 或普通 .nrrd）文件，
    合并到新的数据集中。

    Parameters
    ----------
    reference_dataset : str
        参考数据集路径，例如 "/date/yifanchen/data/Uterus_Ovary_CT_train_val_test"
    datasets_to_merge : list[str]
        待合并数据集路径列表，例如
        ["/date/yifanchen/data_each_organ/CPTAC-UCEC",
         "/date/yifanchen/data_each_organ/TCGA-OV"]
    output_root : str
        新数据集存放的根目录，默认 "/date/yifanchen/data_mask"
    """

    dataset_name = os.path.basename(reference_dataset.rstrip("/"))
    output_dataset = os.path.join(output_root, dataset_name)
    os.makedirs(output_dataset, exist_ok=True)

    # 1. 创建 train / val / test 子目录
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_dataset, subset), exist_ok=True)

    print(f"🟢 创建输出数据集: {output_dataset}")

    # 2. 遍历参考数据集的 train / val / test 结构
    for subset in ["train", "val", "test"]:
        ref_subset_path = os.path.join(reference_dataset, subset)
        out_subset_path = os.path.join(output_dataset, subset)

        if not os.path.isdir(ref_subset_path):
            print(f"⚠️ 参考数据集缺少 {subset} 文件夹: {ref_subset_path}")
            continue

        for case_name in sorted(os.listdir(ref_subset_path)):
            ref_case_path = os.path.join(ref_subset_path, case_name)
            if not os.path.isdir(ref_case_path):
                continue

            for period_name in sorted(os.listdir(ref_case_path)):
                ref_period_path = os.path.join(ref_case_path, period_name)
                if not os.path.isdir(ref_period_path):
                    continue

                dest_period_path = os.path.join(out_subset_path, case_name, period_name)
                os.makedirs(dest_period_path, exist_ok=True)

                # 在所有待合并数据集中查找对应病例和时期
                found = False
                for src_dataset in datasets_to_merge:
                    src_period_path = os.path.join(src_dataset, "CT", case_name, period_name)
                    if not os.path.isdir(src_period_path):
                        continue

                    # 复制三个必需文件
                    for f in os.listdir(src_period_path):
                        if (f.endswith("_CT.nii") or
                            f.endswith("_CTC.nii") or
                            f.endswith(".nrrd")):   # 包括 .seg.nrrd
                            shutil.copy2(
                                os.path.join(src_period_path, f),
                                os.path.join(dest_period_path, f)
                            )
                    found = True
                    break  # 找到后不再检查其它数据集

                if not found:
                    print(f"❌ 未在任何源数据集找到: {case_name}/{period_name}")

    print(f"🎉 合并完成，新数据集位于: {output_dataset}")


# ========== 示例调用 ==========
if __name__ == "__main__":
    reference = "/date/yifanchen/data/Stomach_Colon_Liver_Pancreas_CT_train_val_test"
    sources = [
        "/date/yifanchen/data_each_organ/colon/CMB-CRC",
        "/date/yifanchen/data_each_organ/colon/TCGA-COAD",
        "/date/yifanchen/data_each_organ/pancreas/CPTAC-PDA",
        "/date/yifanchen/data_each_organ/stomach/TCGA-STAD",
        "/date/yifanchen/data_each_organ/liver/HCC-TACE-Seg",
        "/date/yifanchen/data_each_organ/liver/TCGA-LIHC"
    ]
    merge_datasets(reference, sources)