# # a='Adrenal_Ki67_Seg_019_2007-12-22_CT.nii'
# # modality='CT'
# # print(a.split(modality)[0])
# import os

# root_dir = "../../data/Stomach_Colon_Liver_Pancreas_CT_train_val_test"

# for dirpath, dirnames, filenames in os.walk(root_dir):
#     # 遍历目录名
#     for dirname in dirnames:
#         if "术后" in dirname:
#             print("目录:", os.path.join(dirpath, dirname))
#     # 遍历文件名
#     for filename in filenames:
#         if "术后" in filename:
#             print("文件:", os.path.join(dirpath, filename))


from PIL import Image
import numpy as np

# 读取图片
img = Image.open("/date/yifanchen/data_no_mask/2D_jpg/Breast_many2one_jpg/dce13_dce2/train/ISPY1_1001_1.png")  # 这里替换成你的图片路径
width, height = img.size

# 计算中间位置（左右拼接时用）
mid = width // 2

# 左半部分
left_img = img.crop((0, 0, mid, height))
left_img.save("left.jpg")

# 右半部分
right_img = img.crop((mid, 0, width, height))
right_img.save("right.jpg")

# 如果你还想查看通道数和形状：
left_arr = np.array(left_img)
right_arr = np.array(right_img)

print("左边图像 shape:", left_arr.shape)   # (H, W, C)
print("右边图像 shape:", right_arr.shape)   # (H, W, C)