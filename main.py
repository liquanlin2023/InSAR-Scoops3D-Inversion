"""
1.生成内摩擦角，粘聚力
2.修改参数文件，修改内摩擦角，粘聚力，输入：一对内摩擦角，粘聚力，输出none，执行修改参数文件任务
3.run_exe函数，输入：exe参数文件，，输出none，执行软件计算，生成安全系数文件
4.将栅格文件转化问array数组，输入：栅格，输出array,main中调用生成landslide_labels,safety_scores
5.计算auc值，输入：landslide_label,safety_score
6.保存每一次的内摩擦角，粘聚力，auc值，定义全局变量friction_cohe_auc_list[]
7.将字段保存如excel中
8.作图，画出三维散点图，拟合散点做出曲面，找到曲面的最大值点，得到，粘聚力，内摩擦角，
"""



from config import cohesion_range, friction_range
from parall_task import parall_task
import multiprocessing
from material import create_3d_material_file
from optimal_params import optimal_params
from validation import validation
from zonal_result_calcu import zonal_result_calcu
import tkinter as tk
from GUI import ParameterGUI



if __name__ == '__main__':
    root = tk.Tk()
    app = ParameterGUI(root)
    root.mainloop()
    #多进程中的全局变量变量共享，需要使用Manager共享全局变量，列表才能append
    manager = multiprocessing.Manager()
    result_list_0 = manager.list()
    result_list_1 = manager.list()
    result_list_2 = manager.list()
    result_list_3 = manager.list()
    result_list_4 = manager.list()

    cpu_count = multiprocessing.cpu_count()
    print(f"计算机上cpu个数为:{cpu_count}")
    #进程池
    pool = multiprocessing.Pool(processes=12)

    # 外层循化，循环粘聚力
    for cohesion in cohesion_range:
        # 内层循环
        for friction in friction_range:
            pool.apply_async(func=parall_task, args=(cohesion, friction,result_list_0,result_list_1,result_list_2,result_list_3,result_list_4))
            #parall_task(cohesion,friction)

    pool.close()
    pool.join()

    # 生成最优参数的 CSV 文件路径
    optimal_params_csv_path = optimal_params()

    create_3d_material_file(optimal_params_csv_path)
    # 使用生成的 CSV 文件路径创建 3D 材料文件

    # 分区分工况计算
    zonal_result_calcu()

    #验证
    validation()