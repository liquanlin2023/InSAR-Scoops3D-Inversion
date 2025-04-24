import pandas as pd
import os

from config import zonal_excel_result_path

def optimal_params():
    """
    在多个 CSV 文件中查找具有特定粘聚力且召回率和总正确率都大于 0.5 的行，
    并从中找到面积比最小的行，提取其粘聚力和内摩擦角，添加分区信息，返回包含这些信息的数据框，
    并保存为 CSV 文件。

    参数:
    无

    返回:
    str: 生成的 CSV 文件路径
    """
    file_paths = [
        f"{zonal_excel_result_path}/全区域结果表.csv",
        f"{zonal_excel_result_path}/松散岩组结果表.csv",
        f"{zonal_excel_result_path}/软弱岩组结果表.csv",
        f"{zonal_excel_result_path}/软硬组合岩组结果表.csv",
        f"{zonal_excel_result_path}/硬岩组结果表.csv"
    ]

    cohesion_values = [14, 13, 14, 15, 16]

    optimal_params = []

    for file_path, cohesion in zip(file_paths, cohesion_values):
        # 读取 CSV 文件到 DataFrame
        df = pd.read_csv(file_path)

        # 筛选指定粘聚力的行
        df_with_specific_cohesion = df[df['粘聚力/kPa'] == cohesion]

        # 筛选召回率和总正确率都大于 0.5 的行
        filtered_df = df_with_specific_cohesion[(df_with_specific_cohesion['召回率'] > 0.5) & (df_with_specific_cohesion['总正确率'] > 0.5)]

        # 如果没有符合条件的行，继续处理下一个文件
        if filtered_df.empty:
            continue

        # 找到面积比最小的行
        optimal_row = filtered_df.loc[filtered_df['面积比'].idxmin()]

        # 提取对应的粘聚力和内摩擦角，并添加分区信息
        partition = file_paths.index(file_path)
        file_name = os.path.basename(file_path)
        optimal_params.append((optimal_row['粘聚力/kPa'], optimal_row['内摩擦角/°'], partition, file_name))

    # 创建一个数据框来保存最优参数
    optimal_params_df = pd.DataFrame(optimal_params, columns=['cee', 'phi', '分区', '文件名'])

    # 生成的 CSV 文件路径
    output_csv_path = f'{zonal_excel_result_path}/最优岩土参数.csv'

    # 打印结果并保存为 CSV 文件
    print(optimal_params_df)
    optimal_params_df.to_csv(output_csv_path, index=False)

    return output_csv_path
