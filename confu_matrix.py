
import numpy as np

def confu_matrix(labels, predictions):
    """
    假定安全系数在0到1时预测为滑坡，计算此时的混淆矩阵,及其评估指标
    :param labels: 标签布尔数组
    :param predictions: 预测布尔数组
    :return: TP, TN, FP, FN, precision, recall, accuracy,ratio
    """
    TP = np.sum(np.logical_and(labels, predictions))
    TN = np.sum(np.logical_and(np.logical_not(labels), np.logical_not(predictions)))
    FP = np.sum(np.logical_and(np.logical_not(labels), predictions))
    FN = np.sum(np.logical_and(labels, np.logical_not(predictions)))
    N = TP + TN + FP + FN
    #精确率
    precision = round(TP / (TP + FP),2)
    #召回率
    recall = round(TP / (TP + FN),2)
    #总正确率
    accuracy = round((TP + TN) / (TP + TN + FP + FN),2)
    #F1_score
    F1_score = round(2 * precision * recall / (precision + recall),2)
    #面积比： 预测出的滑坡是真实滑坡的几倍？
    ratio = round(np.sum(predictions)/np.sum(labels),2)
    #最大面积比
    ratio_max = round(np.sum(N/(TP+FN)),2)

    #预测出的滑坡区占全区的比值
    predict_landslide_propotion = round((TP + FP) / N, 2)

    # print("精确率:", "{:.2f}%".format(precision*100))
    # print("召回率:", "{:.2f}%".format(recall*100))
    # print("总正确率:","{:.2f}%".format(accuracy*100) )
    # print("F1_score:","{:.2f}%".format(F1_score*100))
    # print("面积比:", "{:.2f}".format(ratio))
    return TP, TN, FP, FN, N, precision, recall, accuracy, F1_score, ratio,ratio_max, predict_landslide_propotion






