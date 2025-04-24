import os

from config import scoops3d_param_file_path, directory


def modify_param(cohesion,friction):
    """
    修改scp参数文件，组要修改文件中的内摩擦角与粘聚力值
    :param cohesion:粘聚力
    :param friction:内摩擦角
    :return:修改后的文件名称
    """
    #读取参数文件
    with open(scoops3d_param_file_path,"r") as file:
        lines=file.readlines()
    #修改第11行的第一个参数和第二个参数
    if len(lines)>=11:
        line=lines[9].split('   ')
        if len(line) >=2 :
            #单位转化，此处不需要乘以1000
            line[1]=str(cohesion)
            line[2]=str(friction)
            lines[9]='   '.join(line).strip()+'  \n'
        line = lines[-1].split('\\')
        line[-2] = "output"+f"_cee_{cohesion}"+f"_fhi_{friction}"
        lines[-1] = '\\'.join(line).strip()+'\n'

    new_directory = directory[:-1]
    input_param_file_path = new_directory + "input"+f"_cee_{cohesion}"+f"_fhi_{friction}.scp"


    #写回修改后的内容到参数文件
    with open(input_param_file_path,'w') as file:
         file.writelines(lines)

    # 在屏幕上显示参数已修改
    print(f'参数文件已修改\nc=:{cohesion}\nphi=:{friction}')
    return line[-2],input_param_file_path