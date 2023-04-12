# -*- coding: utf-8 -*-
 
# try:
import cv2
# except:
#     import sys
#     sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
#     import cv2
 
import numpy as np
import os
import time
 
 
def TIF_algo(p1, p2, median_blur_value=3, mean_blur_value=35):
    """
    通过TIF方法融合图像
    :param p1_path: 图像1路径
    :param p2_path: 图像2路径
    :param median_blur_value: 中值滤波参数
    :param mean_blur_value:  均值滤波参数
    :return: 融合图像
    """
    # median_blur_value = 3  # 中值滤波系数
    # mean_blur_value = 35  # 均值滤波系数
 
    # 均值滤波后(35,35)的图层，即基础层
    p1_b = cv2.blur(p1, (mean_blur_value, mean_blur_value))
    p1_b = p1_b.astype(np.float)  # 转成float类型矩阵
    p2_b = cv2.blur(p2, (mean_blur_value, mean_blur_value))
    p2_b = p2_b.astype(np.float)  # 转成float类型矩阵
    # cv2.imshow('picture after mean blur p1_b', p1_b)
    # cv2.imshow('picture after mean blur p2_b', p2_b)
    # 均值滤波后的细节层
    # p1_d = abs(p1.astype(np.float) - p1_b)
    # p2_d = abs(p2.astype(np.float) - p2_b)
    p1_d = p1.astype(np.float) - p1_b
    p2_d = p2.astype(np.float) - p2_b
    # cv2.imshow('detail layer p1', p1_d / 255.0)
    # cv2.imshow('detail layer p2', p2_d / 255.0)
    # 原图经过中值滤波后的图层
    p1_after_medianblur = cv2.medianBlur(p1, median_blur_value)
    p2_after_medianblur = cv2.medianBlur(p2, median_blur_value)
    # 矩阵转换,换成float型，参与后面计算
    p1_after_medianblur = p1_after_medianblur.astype(np.float)
    p2_after_medianblur = p2_after_medianblur.astype(np.float)
 
    # 计算均值和中值滤波后的误差
    p1_subtract_from_median_mean = p1_after_medianblur - p1_b + 0.01  # 加0.01 保证结果非NAN
    p2_subtract_from_median_mean = p2_after_medianblur - p2_b + 0.01
    # cv2.imshow('subtract_from_median_mean  p1_subtract_from_median_mean', p1_subtract_from_median_mean/255.0)
    # cv2.imshow('subtract_from_median_mean  p2_subtract_from_median_mean', p2_subtract_from_median_mean/255.0)
    m1 = p1_subtract_from_median_mean[:, :, 0]
    m2 = p1_subtract_from_median_mean[:, :, 1]
    m3 = p1_subtract_from_median_mean[:, :, 2]
    res = m1 * m1 + m2 * m2 + m3 * m3
    # delta1 = np.sqrt(res)
    delta1 = res
    m1 = p2_subtract_from_median_mean[:, :, 0]
    m2 = p2_subtract_from_median_mean[:, :, 1]
    m3 = p2_subtract_from_median_mean[:, :, 2]
    res = m1 * m1 + m2 * m2 + m3 * m3
    # delta2 = np.sqrt(res) #采用平方和开根号做权重计算
    # delta2 = res #采用平方和做权重计算
    delta2 = abs(m1)  # 由于图像2 红外图像是灰度图像，直接用像素差做权重计算
 
    delta_total = delta1 + delta2  # 分母
 
    psi_1 = delta1 / delta_total
    psi_2 = delta2 / delta_total
    psi1 = np.zeros(p1.shape, dtype=np.float)
    psi2 = np.zeros(p2.shape, dtype=np.float)
    psi1[:, :, 0] = psi_1
    psi1[:, :, 1] = psi_1
    psi1[:, :, 2] = psi_1
    psi2[:, :, 0] = psi_2
    psi2[:, :, 1] = psi_2
    psi2[:, :, 2] = psi_2
    # 基础层融合
    p_b = 0.5 * (p1_b + p2_b)
    # 细节层融合
    p_d = psi1 * p1_d + psi2 * p2_d
    # 整体融合
    p = p_b + p_d
    return p
 
if __name__ == '__main__':
    # 程序开始时的时间
    time_start = time.time()
    # 1 图表示可见光；2 图表示红外
    #flist()

    visible_path = 'kaist_wash/kaist_wash_picture_train/visible'  # 可见光图像
    lwir_path    = 'kaist_wash/kaist_wash_picture_train/lwir'  # 红外图像
    TIF_path     = r'kaist_wash/TIF_picture'
    flist1       = os.listdir(visible_path)
    flist2       = os.listdir(lwir_path)
    for i in range(0,len(flist1)):
        p1_path = os.path.join(visible_path,flist1[i])
        p2_path = os.path.join(lwir_path,flist2[i])
        p1 = cv2.imread(p1_path, cv2.IMREAD_COLOR)#.astype(np.float)
        p2 = cv2.imread(p2_path, cv2.IMREAD_COLOR)#.astype(np.float)
        p = TIF_algo(p1, p2)#融合
        cv2.imwrite(os.path.join(TIF_path,flist1[i]), p)
    time_end = time.time()
    print('程序运行花费时间', time_end - time_start)