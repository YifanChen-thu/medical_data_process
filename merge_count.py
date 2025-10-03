import os

def count_cases_periods(merged_dataset):
    """
    统计输出数据集 train / val / test
    - 每个子集中病例数
    - 每个子集中所有时期数
    - 以及总计
    """
    total_cases = 0
    total_periods = 0

    print(f"=== 数据集统计：{merged_dataset} ===")
    for subset in ["train", "val", "test"]:
        subset_path = os.path.join(merged_dataset, subset)
        if not os.path.isdir(subset_path):
            print(f"⚠️ 缺少 {subset} 文件夹")
            continue

        case_count = 0
        period_count = 0

        for case_name in os.listdir(subset_path):
            case_path = os.path.join(subset_path, case_name)
            if not os.path.isdir(case_path):
                continue
            case_count += 1
            for period_name in os.listdir(case_path):
                period_path = os.path.join(case_path, period_name)
                if os.path.isdir(period_path):
                    period_count += 1

        total_cases += case_count
        total_periods += period_count

        print(f"{subset}: 病例 {case_count}  | 时期 {period_count}")

    print("------ 总计 ------")
    print(f"病例总数: {total_cases}")
    print(f"时期总数: {total_periods}")



# ===== 示例调用 =====
if __name__ == "__main__":
    merged = '/date/yifanchen/data_mask/all_ct_mask_nii'
    count_cases_periods(merged)