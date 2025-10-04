import pickle

def inspect_split_pkl(pkl_path):
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    print(f"Type of data: {type(data)}")
    if isinstance(data, list):
        print(f"Total folds: {len(data)}\n")
        for fold_idx, fold in enumerate(data):
            print(f"=== Fold {fold_idx} ===")
            for split in ["train", "val", "test"]:
                if split in fold:
                    n_cases = len(fold[split])
                    print(f"  {split}: {n_cases} cases")
                    # 打印前 3 个样例看看路径
                    for i, (case_id, paths) in enumerate(fold[split].items()):
                        print(f"    {case_id}: {paths}")
                        if i >= 2:  # 只展示前 3 个
                            break
            print()
    elif isinstance(data, dict):
        print("Top-level dict keys:", data.keys())
        for k, v in data.items():
            print(f"{k}: {type(v)}")
    else:
        print("Unknown structure:", type(data))


if __name__ == "__main__":
    # pkl_path = "/date/yifanchen/data_mask/all_ct_mask_nii/split.pkl"
    pkl_path= "/date/yifanchen/data_mask/Breast_dce_train_val_test_nii_mask/split.pkl"
    inspect_split_pkl(pkl_path)