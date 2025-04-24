from config import  zones_file_path,slow_moving_landslide_shp_flie_path,slow_moving_landslide_asc_file
import numpy as np
from convert_shp_to_asc import convert_shp_to_asc



#将滑坡shp文件转为asc文件
slow_moving_landslide_flie_path = convert_shp_to_asc(slow_moving_landslide_shp_flie_path,slow_moving_landslide_asc_file)
#一次性读入滑坡ascii文件数据，使其成为全局变量
landslide_grid=np.loadtxt(slow_moving_landslide_asc_file,skiprows=6)

#读入岩组分区ascii文件，
# 当需要反演到某一岩组区域时，取出分区的索引下标即可，不需要分4个区域单独反演
zones_grid = np.loadtxt(zones_file_path , skiprows = 6)



def raster2array(safety_grid_file_path):
    """
    将栅格文件配准
    :param safety_grid_file_path: 安全系数栅格路径
    :return:安全系数值，滑坡标签值，安全系数分类值，岩组分区值
    """

    #读取安全系数文件，
    safety_grid=np.loadtxt(safety_grid_file_path,skiprows=6)



    #将-9999值改为NaN
    safety_grid[safety_grid == 9999.0000] = np.nan

    # 将滑坡文件中的有效值设为1
    landslide_grid[landslide_grid != -9999] = 1


    # 将安全系数文件和滑坡文件展平为一维数组
    safety_scores = safety_grid.flatten()
    landslide_labels = landslide_grid.flatten()

    #将岩组分区文件展平为一维数组
    zones_labels = zones_grid.flatten()




    #去除NaN值,索引到有效值,valid_indices:为一维bool数组
    valid_indices = ~np.isnan(safety_scores)
    safety_scores = safety_scores[valid_indices]
    zones_labels = zones_labels[valid_indices]


    #标签为0，1
    landslide_labels = landslide_labels[valid_indices]
    #将标签变为bool数组
    landslide_labels = landslide_labels > 0

    #bool数组 安全系数0到1的预测滑坡区
    safety_scores_0_1 =  safety_scores < 1

    return safety_scores,landslide_labels , safety_scores_0_1 ,zones_labels



