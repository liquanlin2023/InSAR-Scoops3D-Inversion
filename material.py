import pandas as pd
import numpy as np
import rasterio
from config import zones_file_path, dem_asc_file, material_file_path


def create_3d_material_file(optimal_params_csv_path):
    """
    生成 3D 材料文件的函数，使用给定的最优参数 CSV 文件路径。

    参数:
    optimal_params_csv_path (str): 最优参数 CSV 文件路径

    返回:
    无
    """
    # 从 CSV 文件中读入最优参数数据框
    optimal_params_df = pd.read_csv(optimal_params_csv_path)

    # 读入岩组分区数据
    with rasterio.open(zones_file_path) as dataset_zone:
        zone_array = dataset_zone.read(1)

    # 读入高程文件
    with rasterio.open(dem_asc_file) as dataset_dem:
        dem_array = dataset_dem.read(1)
        # 将无效值替换为 0
        dem_array = np.where(dem_array == dataset_dem.nodata, 0, dem_array)

    # 栅格行列数
    num_rows, num_columns = zone_array.shape

    # 创建一个字典来保存各个分区的最优参数
    params_dict = optimal_params_df.set_index('分区')[['cee', 'phi']].to_dict(orient='index')
    print("正在生成3d_material.txt...")


    # 遍历所有栅格数组并进行编号，转为 3D 材料
    with open(material_file_path, 'w') as f:
        # 写入头文件信息
        header = (
            "# 3D material properties file for Scoops3D example C\n"
            "# Arai and Tagyo example 2\n"
            "# irregular vertical spacing, ijz coordinates\n"
            "#\n"
            "#  i j z cee   phi\n"
            "#\n"
            "coords\n"
            "ijz\n"
            "zlocation\n"
            "bottom\n"
        )
        f.write(header)

        for y in range(num_rows):
            for x in range(num_columns):
                # 读入每个栅格高程信息
                height = dem_array[y, x]
                # 获取当前栅格的分区号
                zone = zone_array[y, x]

                # 根据分区号从参数字典中获取对应的粘聚力和内摩擦角
                if zone in params_dict:
                    cee = params_dict[zone]['cee']
                    phi = params_dict[zone]['phi']
                else:
                    # 对于无效值区域，岩土参数任意给定一个
                    cee = 0
                    phi = 0

                # 输出编号和栅格的高程值以及岩土参数
                f.write(f"   {x + 1}  {y + 1}  {0}  {cee}  {phi} {16}\n")
                f.write(f"   {x + 1}  {y + 1}  {height}  {cee}  {phi} {16}\n")
    print("3d_material.txt生成成功！")
