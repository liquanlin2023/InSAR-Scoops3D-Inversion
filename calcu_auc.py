import numpy as np
from sklearn.metrics import roc_auc_score


def calcu_acu(safety_scores,landslide_labels):
    """
    计算一对粘聚力，内摩擦角roc曲线下的面积auc,
    :param safety_scores: 安全系数 类型为ndarray
    :param landslide_labels: 滑坡标签 类型为ndarray
    :return: 返回auc计算值
    """
    #计算全区域的auc值

    #需要交换滑坡的0和1，因为预测值约越小约代表为滑坡
    landslide_labels = np.logical_not(landslide_labels)


    auc = roc_auc_score(landslide_labels,safety_scores)

    return auc