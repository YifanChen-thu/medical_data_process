import os
import scipy.io
import nibabel as nib
import numpy as np

def save_dce_only(mat_path, output_dir):
    """
    只保存 dce1/dce2/dce3/tumor/tumor1
    """
    os.makedirs(output_dir, exist_ok=True)
    
    mat_data = scipy.io.loadmat(mat_path)
    
    img_resolution = mat_data.get('img_resolution', None)
    if img_resolution is None:
        raise KeyError(f"{mat_path} 缺少 img_resolution")
    img_resolution = img_resolution.squeeze()
    
    affine = np.diag(np.append(img_resolution, 1.0))
    
    dce_keys = ['dce1', 'dce2', 'dce3', 'tumor', 'tumor1']
    
    for key in dce_keys:
        if key in mat_data:
            data = mat_data[key].astype(np.float32)
            nii_img = nib.Nifti1Image(data, affine)
            save_path = os.path.join(output_dir, f"{output_dir.split('/')[-1]}_{key}.nii")
            nib.save(nii_img, save_path)
            print(f"✅ 保存 {save_path}")
        else:
            print(f"⚠️ 警告：{mat_path} 中缺少 {key}")


def batch_convert_dce_only(input_root, output_root):
    """
    批量处理 train/val/test 文件夹中的 .mat 文件，只保存 dce1/dce2/dce3/tumor/tumor1
    """
    for split in ['train', 'val', 'test']:
        input_dir = os.path.join(input_root, split)
        output_dir_base = os.path.join(output_root, split)
        os.makedirs(output_dir_base, exist_ok=True)
        
        mat_files = [f for f in os.listdir(input_dir) if f.endswith('.mat')]
        print(f"\n=== 处理 {split} 文件夹，共 {len(mat_files)} 个 .mat 文件 ===")
        
        for mat_file in mat_files:
            mat_path = os.path.join(input_dir, mat_file)
            output_dir = os.path.join(output_dir_base, mat_file.split('.mat')[0])
            save_dce_only(mat_path, output_dir)


input_root = '../../data/Breast_MR_train_val_test/'
output_root = '/date/yifanchen/data_mask/Breast_dce_train_val_test_nii_mask'

batch_convert_dce_only(input_root, output_root)