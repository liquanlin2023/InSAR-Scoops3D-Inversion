"""
功能：将历史滑坡转为点，将每种工况下分区计算结果分级，统计每个级别中滑坡点个数，滑坡点密度，将统计结果存入表格。
# 1. 将历史滑坡面文件转为滑坡点文件
# 2. 将天然状态下，0.1g，0.15g工况下结果分为多个等级，统计每个等级下滑坡点个数
"""

import os
import rasterio
import geopandas as gpd
import pandas as pd
from config import landslide, result_file_path, zonal_result_calcu_path


# 1. 将历史滑坡面文件转为滑坡点文件
def convert_polygon_to_point(input_shapefile, output_shapefile, target_crs_epsg=32648):
    # 读取面文件
    polygons = gpd.read_file(input_shapefile)

    # 创建一个空的 GeoDataFrame 用于存储点
    points = gpd.GeoDataFrame(columns=['geometry'], crs=polygons.crs)

    # 计算每个面的中心点并存储到新的 GeoDataFrame 中
    points['geometry'] = polygons['geometry'].centroid

    # 如果需要保留原始属性，可以将其合并到新的点文件中
    for col in polygons.columns:
        if col != 'geometry':
            points[col] = polygons[col]

    # 将点文件投影转换为 UTM 48N
    points = points.to_crs(epsg=target_crs_epsg)

    # 将点文件保存为新的 shapefile
    points.to_file(output_shapefile, driver='ESRI Shapefile')


def validation():
    # 示例用法
    input_shapefile = landslide
    output_folder = os.path.join(result_file_path, '滑坡点')

    # 创建目标文件夹
    os.makedirs(output_folder, exist_ok=True)

    output_shapefile = os.path.join(output_folder, '滑坡点.shp')

    convert_polygon_to_point(input_shapefile, output_shapefile)
    print(f"Point shapefile saved to: {output_shapefile}")

    # 2. 将天然状态下，0.1g，0.15g工况下结果分为多个等级，统计每个等级下滑坡点个数

    # 递归搜索zonal_result_calcu_path路径下的所有子文件夹，找到以fos3d_out.asc结尾的文件
    asc_files = []
    for root, dirs, files in os.walk(zonal_result_calcu_path):
        for file in files:
            if file.endswith("_fos3d_out.asc"):
                asc_files.append(os.path.join(root, file))

    # 打印找到的ASC文件名
    print("找到的ASC文件:")
    for asc_file in asc_files:
        print(asc_file)

    # 打开SHP点文件
    shp_file = output_shapefile
    shp_data = gpd.read_file(shp_file)

    # 指定目标坐标系为UTM Zone 48N
    target_crs = 'EPSG:32648'

    # 将SHP点投影到UTM Zone 48N坐标系中
    shp_data_proj = shp_data.to_crs(target_crs)

    # 初始化结果列表
    results = []

    # 定义工况顺序
    conditions = ["天然状态", "0.1g", "0.15g"]

    # 处理每个asc文件
    for i, asc_file in enumerate(asc_files):
        print(f"正在处理文件: {asc_file}")  # 打印正在处理的ASC文件名
        with rasterio.open(asc_file) as src:
            asc_data = src.read(1)  # 读取第一个波段的数据
            asc_transform = src.transform  # 获取变换信息
            nodata_value = src.nodata  # 获取NODATA值
            pixel_size = abs(asc_transform.a)  # 获取像素大小

        # 像素面积
        pixel_area = pixel_size * pixel_size / 1000000  # 平方千米

        # 根据文件顺序分配工况
        condition = conditions[i % len(conditions)]

        # 初始化区间统计字典
        interval_counts = {'0到0.75': 0, '0.75到1': 0, '大于1': 0}
        interval_areas = {'0到0.75': 0, '0.75到1': 0, '大于1': 0}

        # 循环遍历每个点并获取栅格值
        for index, point in shp_data_proj.iterrows():
            x = point.geometry.x
            y = point.geometry.y

            # 将点的坐标转换为栅格坐标
            row, col = src.index(x, y)

            # 获取该栅格上的值
            value = asc_data[row, col]

            # 判断栅格值所在的区间并统计
            if value != nodata_value:  # 跳过NODATA值
                if value >= 0 and value <= 0.75:
                    interval_counts['0到0.75'] += 1
                elif value > 0.75 and value <= 1:
                    interval_counts['0.75到1'] += 1
                elif value > 1:
                    interval_counts['大于1'] += 1

        # 记录每个asc文件的结果，并添加 "工况" 列
        results.append({
            '工况': condition,
            '文件': asc_file,
            '0到0.75 (个数)': interval_counts['0到0.75'],
            '0.75到1 (个数)': interval_counts['0.75到1'],
            '大于1 (个数)': interval_counts['大于1']
        })

    # 将结果转换为DataFrame
    results_df = pd.DataFrame(results)

    # 处理每个asc文件并计算面积
    for i, asc_file in enumerate(asc_files):
        print(f"正在处理文件: {asc_file}")  # 打印正在处理的ASC文件名
        with rasterio.open(asc_file) as src:
            asc_data = src.read(1)  # 读取第一个波
            asc_transform = src.transform # 获取变换信息
            nodata_value = src.nodata # 获取NODATA值
            pixel_size = abs(asc_transform.a) # 获取像素大小
            # 像素面积
            pixel_area = pixel_size * pixel_size / 1000000  # 平方千米

            # 初始化区间面积统计字典
            interval_areas = {'0到0.75': 0, '0.75到1': 0, '大于1': 0}
            interval_counts = {'0到0.75': 0, '0.75到1': 0, '大于1': 0}

            # 循环遍历每个栅格并统计栅格值
            for row in asc_data:
                for value in row:
                    if value != nodata_value:  # 跳过NODATA值
                        if value >= 0 and value <= 0.75:
                            interval_counts['0到0.75'] += 1
                        elif value > 0.75 and value <= 1:
                            interval_counts['0.75到1'] += 1
                        elif value > 1:
                            interval_counts['大于1'] += 1

            # 计算每个区间的面积
            for interval, count in interval_counts.items():
                interval_areas[interval] = count * pixel_area

            # 更新结果 DataFrame
            results_df.loc[i, '0到0.75 (平方千米)'] = interval_areas['0到0.75']
            results_df.loc[i, '0.75到1 (平方千米)'] = interval_areas['0.75到1']
            results_df.loc[i, '大于1 (平方千米)'] = interval_areas['大于1']

        # 计算滑坡点密度，并保留2位小数
        results_df['0到0.75 (点密度)'] = round((results_df['0到0.75 (个数)'] / results_df['0到0.75 (平方千米)']) * 100,
                                               2)
        results_df['0.75到1 (点密度)'] = round((results_df['0.75到1 (个数)'] / results_df['0.75到1 (平方千米)']) * 100,
                                               2)
        results_df['大于1 (点密度)'] = round((results_df['大于1 (个数)'] / results_df['大于1 (平方千米)']) * 100, 2)

        # 指定保存路径
        csv_file_path = os.path.join(result_file_path, "统计结果.csv")

        # 将DataFrame保存为CSV文件
        results_df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

        print("统计结果已保存到:", csv_file_path)
