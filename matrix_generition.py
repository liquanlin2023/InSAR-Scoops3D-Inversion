import pandas as pd

# 读取CSV文件路径
file_path = r'D:\param_inversion\result_MPa\zonal_assessment\全区域结果表.csv'

# 读取CSV文件
data = pd.read_csv(file_path)

# 创建数据透视表，以粘聚力作为列，内摩擦角作为行，F1_score作为值，缺失值填充为0
pivot_table = data.pivot_table(values='总正确率', index='内摩擦角/°', columns='粘聚力/kPa', fill_value=0)

# 保存矩阵为CSV文件
output_path = r'D:\param_inversion\result_MPa\zonal_assessment\全区域矩阵总正确率.csv'
pivot_table.to_csv(output_path, encoding='utf-8-sig')

print(f'矩阵已保存为 {output_path}')