import os
import numpy as np
import nibabel as nib
from PIL import Image
import concurrent.futures
import argparse
import random



def normalize_image(image):
    """归一化图像数据到 0-255 范围。"""
    # 转换为浮点数以避免数据溢出
    image = image.astype(np.float32)

    # 检查 NaN 值并替换为零
    image = np.nan_to_num(image)

    # 获取最大值和最小值
    min_val = np.min(image)
    max_val = np.max(image)

    # 避免除以零的情况
    if max_val - min_val != 0:
        image = (image - min_val) / (max_val - min_val)
    else:
        image = np.zeros(image.shape)

    # 转换为 0-255 范围的 uint8 类型
    image = (image * 255).astype(np.uint8)

    return image

def process_patient(patient_name, split_dir, train_data_dir, test_data_dir, val_data_dir, save_dir_modality, task_mode, modality): #, num_slices):
    


    if split_dir == "test":
        patient_dir = os.path.join(test_data_dir, patient_name)
    elif split_dir == 'train':
        patient_dir = os.path.join(train_data_dir, patient_name)
    elif split_dir == 'val':
        patient_dir = os.path.join(val_data_dir, patient_name)
    
    #period
    patient_period=[]#
    for period_id in os.listdir(patient_dir):
        period_dir = os.path.join(patient_dir, period_id)
        if os.path.isdir(period_dir): #'.DS_Store'
            patient_period.append(period_dir)
    

    if modality == 'CT':
        no_c_suffix = '_CT.nii'
        with_c_suffix = '_CTC.nii'

        for period_period_dir in patient_period:
            for patient_id in os.listdir(period_period_dir):
                new_path=os.path.join(period_period_dir, patient_id)
                
                if patient_id.endswith(no_c_suffix) or patient_id.endswith(with_c_suffix):#其他的文件都不读
                    flag=True
                    if patient_id.endswith(no_c_suffix):
                        no_c_path = new_path
                    elif patient_id.endswith(with_c_suffix):
                        with_c_path = new_path
                else:
                    flag=False

            if flag:     
                # H, W, C
                with_c_data = nib.load(with_c_path).get_fdata()
                no_c_data = nib.load(no_c_path).get_fdata()
                if task_mode=='one2many' or task_mode=='many2one':
                    with_c_2_data = nib.load(with_c_2_data).get_fdata()
                

                total_slices = with_c_data.shape[2]

                # 计算开始和结束的索引以提取中间的100个切片
                # mid_point = total_slices // 2
                # start = max(mid_point - num_slices // 2, 0)
                # end = min(mid_point + num_slices // 2, total_slices)
                # selected_slices = [i for i in range(start, end)]
                # t1c_slices = t1c_data[:, :, selected_slices]
                # t1_slices = t1_data[:, :, selected_slices]
                # t2f_slices = t2f_data[:, :, selected_slices]
                # t2w_slices = t2w_data[:, :, selected_slices]
                if task_mode=='one2one':# one to one tasks
                
                    for idx in range(total_slices):
                        # 将 T2 和 FLAIR 切片转换为 PIL 图像
                        # t2_img_pil = Image.fromarray(normalize_image(t2w_slices[:, :, idx]))
                        # flair_img_pil = Image.fromarray(normalize_image(t2f_slices[:, :, idx]))

                        # 将 T1 和 T1C 切片转换为 PIL 图像
                        t1_img_pil = Image.fromarray(normalize_image(no_c_data[:, :, idx])).rotate(-90, expand=True)
                        t1ce_img_pil = Image.fromarray(normalize_image(with_c_data[:, :, idx])).rotate(-90, expand=True)

                        # 拼接图像 T1 -> T1CE   # L代表灰度图像模式
                        combined_img3 = Image.new('L', (t1_img_pil.width + t1ce_img_pil.width, t1_img_pil.height))
                        combined_img3.paste(t1_img_pil, (0, 0))
                        combined_img3.paste(t1ce_img_pil, (t1_img_pil.width, 0))

                        # 保存图像
                        if patient_id.split(modality)[0]=='.DS_Store':
                            import pdb;pdb.set_trace()
                        combined_img3.save(os.path.join(save_dir_modality, split_dir, f"{patient_id.split(modality)[0]}{idx}.jpg"))
                elif task_mode=='one2many':#many to one tasks
                    pass
                elif task_mode=='many2one':# many to one tasks
                    pass
    # 
    # for idx in range(num_slices):
    #     # 将 T1, FLAIR, T2 切片转换为 PIL 图像并调整到相同的数据范围
    #     t2_img_pil = Image.fromarray(normalize_image(t2w_slices[:, :, idx]))
    #     flair_img_pil = Image.fromarray(normalize_image(t2f_slices[:, :, idx]))
    #     t1n_img_pil = Image.fromarray(normalize_image(t1n_slices[:, :, idx]))

    #     # 拼接图像 T1 -> FLAIR -> T2 RGB三通道
    #     combined_img_left = Image.merge("RGB", (t1n_img_pil, flair_img_pil, t2_img_pil))
    #     combined_img_right = Image.merge("RGB", (t2_img_pil, t2_img_pil, t2_img_pil))
    #     combined_img = Image.new('RGB',
    #                              (combined_img_left.width + combined_img_right.width, combined_img_left.height))
    #     combined_img.paste(combined_img_left, (0, 0))
    #     combined_img.paste(combined_img_right, (combined_img_left.width, 0))
    #     # 拼接图像 T2 -> FLAIR -> T1 RGB三通道
    #     combined_img_left2 = Image.merge("RGB", (t2_img_pil, flair_img_pil, t1n_img_pil))
    #     combined_img_right2 = Image.merge("RGB", (t1n_img_pil, t1n_img_pil, t1n_img_pil))
    #     combined_img2 = Image.new('RGB',
    #                               (combined_img_left2.width + combined_img_right2.width, combined_img_left2.height))
    #     combined_img2.paste(combined_img_left2, (0, 0))
    #     combined_img2.paste(combined_img_right2, (combined_img_left2.width, 0))
    #     # 拼接图像 T1 -> T2 -> FLAIR RGB三通道
    #     combined_img_left3 = Image.merge("RGB", (t1n_img_pil, t2_img_pil, flair_img_pil))
    #     combined_img_right3 = Image.merge("RGB", (flair_img_pil, flair_img_pil, flair_img_pil))
    #     combined_img3 = Image.new('RGB',
    #                               (combined_img_left3.width + combined_img_right3.width, combined_img_left3.height))
    #     combined_img3.paste(combined_img_left3, (0, 0))
    #     combined_img3.paste(combined_img_right3, (combined_img_left3.width, 0))

    #     # 保存图像
    #     combined_img.save(os.path.join(save_dir_t1_flair_t2, split_dir, f"{patient_name}_{idx}.png"))
    #     combined_img2.save(os.path.join(save_dir_t2_flair_t1, split_dir, f"{patient_name}_{idx}.png"))
    #     combined_img3.save(os.path.join(save_dir_t1_t2_flair, split_dir, f"{patient_name}_{idx}.png"))

def prepare_paired(args):
    task_mode=args.task_mode
    modality_modality=args.modality_modality
    modality=args.modality

    dataset_name = args.dataset_name
    output_root = os.path.join(args.output_root, f'{dataset_name.split("_")[0]}_{task_mode}_jpg')
    input_root = os.path.join(args.input_root, dataset_name)

    train_data_dir = os.path.join(input_root,'train')
    val_data_dir = os.path.join(input_root,'val')
    test_data_dir = os.path.join(input_root,'test')

    

    save_dir_modality = os.path.join(output_root, modality_modality)
    # # one  to one tasks CT->CTC, dce1->dce2
    # # many to one tasks dce1,dce3->dce2
    # # one  to many tasks dce1->dce2,3
    os.makedirs(save_dir_modality, exist_ok=True)

    train_split_dir = ["train", "val", "test"]
    for split_dir in train_split_dir:
        os.makedirs(os.path.join(save_dir_modality, split_dir), exist_ok=True)
    #防止和patient id并列的那一层里面有其他的文件
    # import pdb;pdb.set_trace()
    train_patients_name = []
    valid_patients_name = []
    test_patients_name = []
    for train_pre in os.listdir(train_data_dir):
        if os.path.isdir(os.path.join(train_data_dir, train_pre)):
            
            train_patients_name.append(train_pre)
    for val_pre in os.listdir(val_data_dir):
        if os.path.isdir(os.path.join(val_data_dir, val_pre)):
            valid_patients_name.append(val_pre)
    for test_pre in os.listdir(test_data_dir):
        if os.path.isdir(os.path.join(test_data_dir, test_pre)):
            test_patients_name.append(test_pre)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for split_dir in train_split_dir:
            if split_dir == "train":
                patients_name = train_patients_name
            elif split_dir == "val":
                patients_name = valid_patients_name
            elif split_dir == "test":
                patients_name = test_patients_name

            for patient_name in patients_name:
                futures.append(executor.submit(process_patient, patient_name, split_dir, train_data_dir, test_data_dir, val_data_dir, save_dir_modality, task_mode, modality))

        for future in concurrent.futures.as_completed(futures):
            future.result()



if __name__ == '__main__':
    parser = argparse.ArgumentParser('Prepare_Dataset')
    parser.add_argument('--dataset_name', dest='dataset_name', help='dataset_name', type=str,
                        default='Breast_MR_train_val_test_nii_dce_only', required=False)
    parser.add_argument('--output_root', dest='output_root', help='output dir', type=str,
                        default='/date/yifanchen/data_no_mask/2D_jpg', required=False)
    parser.add_argument('--input_root', dest='input_root', help='output dir', type=str,
                        default='/date/yifanchen/data_no_mask/Breast_MR_train_val_test_nii_dce_only/', required=False)    
    parser.add_argument('--modality', dest='modality', help='modality=[CT,DCE]', type=str,
                        default='CT', required=False)
    parser.add_argument('--modality_modality', dest='modality_modality', help='modality=[CT_CTC,dce1_dce2,dce13_dce2,dce1_dce23]', type=str,
                        default='CT_CTC', required=False)
    parser.add_argument('--task_mode', dest='task_mode', help='type of task=[one2one,one2many,many2one]', type=str,
                        default='one2one', required=False)
    

    args = parser.parse_args()

    prepare_paired(args)

"""
python nii2jpg_more_period.py \
  --dataset_name 'Adrenal_CT_train_val_test' \
  --output_root '/date/yifanchen/data_no_mask/2D_jpg' \
  --input_root '../../data' \
  --modality 'CT' \
  --modality_modality 'CT_CTC' \
  --task_mode 'one2one'
python nii2jpg_more_period.py \
  --dataset_name 'Bladder_Kidney_CT_train_val_test' \
  --output_root '/date/yifanchen/data_no_mask/2D_jpg' \
  --input_root '../../data' \
  --modality 'CT' \
  --modality_modality 'CT_CTC' \
  --task_mode 'one2one'
python nii2jpg_more_period.py \
  --dataset_name 'Lung_CT_train_val_test' \
  --output_root '/date/yifanchen/data_no_mask/2D_jpg' \
  --input_root '../../data' \
  --modality 'CT' \
  --modality_modality 'CT_CTC' \
  --task_mode 'one2one'
python nii2jpg_more_period.py \
  --dataset_name 'Stomach_Colon_Liver_Pancreas_CT_train_val_test' \
  --output_root '/date/yifanchen/data_no_mask/2D_jpg' \
  --input_root '../../data' \
  --modality 'CT' \
  --modality_modality 'CT_CTC' \
  --task_mode 'one2one'
python nii2jpg_more_period.py \
  --dataset_name 'Uterus_Ovary_CT_train_val_test' \
  --output_root '/date/yifanchen/data_no_mask/2D_jpg' \
  --input_root '../../data' \
  --modality 'CT' \
  --modality_modality 'CT_CTC' \
  --task_mode 'one2one'
"""

    