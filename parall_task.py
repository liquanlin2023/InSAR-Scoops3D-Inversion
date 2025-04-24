import os
import shutil
import time

import pandas as pd

import calcu_auc
from config import cohesion_range, friction_range, directory, zonal_excel_result_path
from confu_matrix import confu_matrix
from modify_param import modify_param
from raster2array import raster2array
from run_scoops3d_exe import run_scoops3d_exe
#from tqdm import tqdm
import multiprocessing
import threading
from material import create_3d_material_file
from optimal_params import optimal_params
from validation import validation
from zonal_result_calcu import zonal_result_calcu
import tkinter as tk
from GUI import ParameterGUI


#因为多进程的每个进程都要向全局变量写入，为了防止写入冲突，需要lock,当单个进程获取锁，其他进程就不能写入

#预测的滑坡区域占总区域的比值
#多进程multiprocessing
#由于多进程计算完成后会向同一个内存写入计算结果，但不能修改可执行文件的源程序来暂停写入
#打算创建多个保存计算结果的文件夹，防止多进程写入时发生冲突，使得多进程间能够并行计算，需要修改scoops3d参数文件中的保存位置。



#类
#做图
#
# 生成内摩擦角和粘聚力的循环

def parall_task(cohesion,friction,result_list_0,result_list_1,result_list_2,result_list_3,result_list_4):
    """
    执行并行计算函数，包括调用修改岩土参数文件，执行scoops3D可执行文件，
    生成安全系数栅格文件，栅格文件配准，岩组分区，混淆矩阵计算等任务
    :param cohesion: 粘聚力
    :param friction: 内摩擦角
    :param result_list_0: 全区域全局list
    :param result_list_1: 松散岩组全局list
    :param result_list_2: 软弱岩组全局list
    :param result_list_3: 软硬组合岩组全局list
    :param result_list_4: 硬岩组全局list
    :return: none
    """
    # 2 调用modify_param函数，修改参数文件,粘聚力，内摩擦角，输出结果路径，并返回输出路径
    output_name,  input_param_file_path = modify_param(cohesion, friction)

    # 生成输出路径文件夹,scoops3d exe不会自动生成输出文件夹
    output_dir_path = directory + output_name

    if os.path.exists(output_dir_path):
        pass
    else:
        os.makedirs(output_dir_path)

    #结果文件
    result_file = output_name.replace("output","input")+"_fos3d_out.asc"
    result_file_path = os.path.join(output_dir_path,result_file)
    if os.path.exists(result_file_path):
        for filename in os.listdir(output_dir_path):
            file_path = os.path.join(output_dir_path, filename)
            if file_path != result_file_path:
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        # 3执行scoops3D可执行文件，生成安全系数栅格文件
        run_scoops3d_exe(input_param_file_path)
        for filename in os.listdir(output_dir_path):
            file_path = os.path.join(output_dir_path, filename)
            if file_path != result_file_path:
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

    # time.sleep(1)
    print(f"{cohesion,friction}exe计算完成1")

    # 4将计算的栅格文件转为array
    # 每个输出文件夹里的安全系数文件路径
    safety_grid_file_path = output_dir_path + "\input" + f"_cee_{cohesion}" + f"_fhi_{friction}_fos3d_out.asc"
    safety_scores, landslide_labels, safety_scores_0_1, zones_labels = raster2array(safety_grid_file_path)
    print(f"{cohesion,friction}转为array完成2")
    # 循环索引到每个区域
    for zone in range(5):
        # 将滑坡一维数值以及单次安全系数结果一维数组索引到需要计算的岩组区域

        # 如果为5，代表计算全区域，不做索引
        if zone == 0:
            auc = calcu_auc.calcu_acu(safety_scores, landslide_labels)

            # 计算 FS为0到1作为预测滑坡区域的混淆矩阵
            TP, TN, FP, FN, N, precision, recall, accuracy, F1_score, ratio, ratio_max, predict_landslide_propotion = confu_matrix(
                landslide_labels, safety_scores_0_1)
            print(f"{cohesion, friction}混淆矩阵计算完成3")

        else:
            # 1到4分别代表松散岩组，软弱岩组，软硬组合岩组，硬岩组

            safety_scores_index = safety_scores[zones_labels == zone]
            landslide_labels_index = landslide_labels[zones_labels == zone]
            safety_scores_0_1_index = safety_scores_0_1[zones_labels == zone]

            auc = calcu_auc.calcu_acu(safety_scores_index, landslide_labels_index)

            # 计算 FS为0到1作为预测滑坡区域的混淆矩阵
            TP, TN, FP, FN, N, precision, recall, accuracy, F1_score, ratio, ratio_max, predict_landslide_propotion = confu_matrix(
                landslide_labels_index, safety_scores_0_1_index)
            print(f"{cohesion, friction}混淆矩阵计算完成3")

        # 5计算auc值,返回全区域以及每个岩组分区的auc计算值

        # 6将本次循化下的粘聚力，内摩擦角参数以及计算得到的auc值追加到全局列表中去
        # 计算不同的区域需要用不同的列表保存：

        if zone == 0:
            result_list = result_list_0
        elif zone == 1:
            result_list = result_list_1
        elif zone == 2:
            result_list = result_list_2
        elif zone == 3:
            result_list = result_list_3
        else:
            result_list = result_list_4

        result_list.append((
                cohesion, friction, auc, TP, TN, FP, FN, N, precision, recall, accuracy, F1_score, ratio, ratio_max,
                predict_landslide_propotion))
        print(result_list)
        print(f"{cohesion, friction}列表保存完成4")

        # 7将auc结果列表转为excel文件
        df = pd.DataFrame(result_list._getvalue(),
                          columns=['粘聚力/kPa', '内摩擦角/°', 'AUC', '真阳', '真阴', '假阳', '假阴', '总数',
                                   '精确率',
                                   '召回率', '总正确率', 'F1_score', '面积比', '最大面积比', '预测危险区占比'])

        #由于多进程不确定执行的先后顺序，df顺序不对，需要重新排序
        df = df.sort_values(by = ['粘聚力/kPa', '内摩擦角/°'])

        # 将循环变量改为实际的岩组名称，为结果文件命名
        dict_map = {1: "松散岩组", 2: "软弱岩组", 3: "软硬组合岩组", 4: "硬岩组", 0: "全区域"}

        if zone == 0:
            df.to_csv(f"{zonal_excel_result_path}/{dict_map[zone]}结果表.csv", index=False)
        elif zone == 1:
            df.to_csv(f"{zonal_excel_result_path}/{dict_map[zone]}结果表.csv", index=False)
        elif zone == 2:
            df.to_csv(f"{zonal_excel_result_path}/{dict_map[zone]}结果表.csv", index=False)
        elif zone == 3:
            df.to_csv(f"{zonal_excel_result_path}/{dict_map[zone]}结果表.csv", index=False)
        else:
            df.to_csv(f"{zonal_excel_result_path}/{dict_map[zone]}结果表.csv", index=False)
        print(f"{cohesion, friction}csv保存完成5")