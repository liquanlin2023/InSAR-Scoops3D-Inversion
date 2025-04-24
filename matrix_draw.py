import matplotlib.pyplot as plt
plt.rc("font", family="SimHei")

def matrix_draw():
    pass
    # # 绘制正确率和查全率曲线
    # plt.figure()
    # # 创建一个不同的颜色集合，以确保每个 phi 值对应不同的颜色
    # unique_colors = plt.cm.get_cmap('tab10', len(values_phi))
    #
    # # 绘制正确率曲线，为每个 phi 值分配不同的颜色
    # for idx, (value_phi, accuracy_values) in enumerate(phi_curves_accuracy.items()):
    #     color = unique_colors(idx)
    #     plt.plot(values_c, accuracy_values, marker='o', label=f'正确率 (phi={value_phi})', color=color)
    #
    # # 绘制查全率曲线，为每个 phi 值分配不同的颜色
    # for idx, (value_phi, recall_values) in enumerate(phi_curves_recall.items()):
    #     color = unique_colors(idx)
    #     plt.plot(values_c, recall_values, linestyle='dashed', marker='x', label=f'查全率 (phi={value_phi})',
    #              color=color)
    #
    # plt.xlabel('c值')
    # plt.ylabel('比例')
    # plt.title('正确率与查全率变化')
    # plt.legend()
    # plt.grid(True)
    # plt.savefig('accuracy_and_recall_curves.png')
    # plt.show()


