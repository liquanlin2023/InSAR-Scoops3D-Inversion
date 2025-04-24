import subprocess
import time

from config import scoops3d_exe_file_path, scoops3d_param_file_path, cohesion_range, friction_range

#全局变量
# run_times = 0

def run_scoops3d_exe(input_param_file_path):
    """
    调用外部scoops3d可执行程序文件，计算得到物理模型结果
    :param input_param_file_path: 修改岩土参数后的scp文件
    :return: none
    """
    #开启一个子进程，启动scoops3d,获得标准输入，标准输出

    process = subprocess.Popen([scoops3d_exe_file_path],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

    scoops3d_param_file_path_clik = input_param_file_path+'\n'
    #利用标准输入写入scoops3d执行文件路径以及回车
    process.stdin.write(scoops3d_param_file_path_clik)
    process.stdin.flush()
    #
    # start_time = time.time()
    # #运行一次改变一次全局变量
    # global run_times
    # run_times += 1
    # # 从进程的标准输出中实时读取并显示输出
    while True:
        line = process.stdout.readline()
        if not line:
            break  # 如果没有更多输出，则退出循环
        print(line.strip())  # 显示输出
        # time.sleep(4)
        # print(f"共需要搜索{len(cohesion_range) * len(friction_range)}对组合\n", f"正在搜索{run_times}对组合\n", "进度",
        #        "{:.2f}%".format(run_times / (len(cohesion_range) * len(friction_range)) * 100))
        # print('已经用时',"{:.2f}".format((time.time()-start_time)/60),'分钟')
        # time.sleep(2)
        # pycharm里无法清屏，模拟清屏
        # print("\n" * 100)

    process.communicate()




