


import os
from config import material_file_path, zonal_result_calcu_path, scoops3d_param_file_path
from run_scoops3d_exe import run_scoops3d_exe


# 修改scp文件，修改加速度，修改3d_material.txt路径
def modify_scoops3d_param(input_file_path, output_file_path, acceleration):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # 插入内容
    lines.insert(6, "str3d   linterp\n")
    lines.insert(7, "1   0\n")

    # 修改第12行的第二个和第三个数值为-1
    line_12_parts = lines[11].split()
    if len(line_12_parts) >= 3:  # 确保行中有足够的值进行替换
        line_12_parts[1] = '-1'
        line_12_parts[2] = '-1'
    lines[11] = "   ".join(line_12_parts) + '\n'

    # 修改第14行的值为指定加速度
    lines[13] = f"{acceleration}\n"

    # 在倒数第二行插入内容
    lines.insert(-2, "material properties file\n")
    lines.insert(-2, f"{material_file_path}\n")

    # 获取输出文件路径的文件名作为新文件夹名称
    new_folder_name = os.path.splitext(os.path.basename(output_file_path))[0]
    new_folder_path = os.path.join(zonal_result_calcu_path, new_folder_name)

    # 修改最后一行路径
    lines[-1] = f"{new_folder_path}\\"

    # 创建对应的新文件夹，如果不存在
    os.makedirs(new_folder_path, exist_ok=True)

    # 写入到新文件
    with open(output_file_path, 'w') as file:
        file.writelines(lines)

def zonal_result_calcu():
    # 示例用法
    input_file_path = scoops3d_param_file_path

    # 输出文件路径
    output_file_path_0 = f"{zonal_result_calcu_path}\\scoops3d_param_modified_0.scp"
    output_file_path_01 = f"{zonal_result_calcu_path}\\scoops3d_param_modified_0.1.scp"
    output_file_path_015 = f"{zonal_result_calcu_path}\\scoops3d_param_modified_0.15.scp"

    # 生成文件
    modify_scoops3d_param(input_file_path, output_file_path_0, 0)
    modify_scoops3d_param(input_file_path, output_file_path_01, 0.1)
    modify_scoops3d_param(input_file_path, output_file_path_015, 0.15)

    print(f"Files saved to:\n{output_file_path_0}\n{output_file_path_01}\n{output_file_path_015}")

    # 调用scoop3d可执行程序分别计算
    run_scoops3d_exe(output_file_path_0)
    run_scoops3d_exe(output_file_path_01)
    run_scoops3d_exe(output_file_path_015)




