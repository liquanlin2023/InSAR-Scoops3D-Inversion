#scoops3d输入文件
scoops3d_param_file_path = r"D:\param_inversion\source_file\scoops3d_param.scp"

#高程文件
dem_asc_file = r"D:\param_inversion\source_file\dem.asc"

# scoop3d执行文件
scoops3d_exe_file_path = r'D:\param_inversion\source_file\Scoops3D_1.1win64.exe'


# insar滑坡shp文件
# slow_moving_landslide_shp_flie_path = r"D:\param_inversion\source_file\滑坡合并\滑坡合并.shp"
slow_moving_landslide_shp_flie_path = r"D:\param_inversion\source_file\历史滑坡\历史滑坡.shp"

#历史滑坡,用来验证
landslide = r"D:\param_inversion\source_file\历史滑坡\历史滑坡_Project.shp"

#设置滑坡asc路径
slow_moving_landslide_asc_file =  r"D:\param_inversion\result\滑坡.asc"

#岩组分区栅格
zones_file_path = r"D:\param_inversion\source_file\zones.asc"


#分区岩土材料参数文件路径预设置
material_file_path = r'D:\param_inversion\result\3D_material.txt'


#结果输出路径
directory = r"D:\param_inversion\result\scoops3d_result\\"


result_file_path = r"D:\param_inversion\result"


#分区评估表格输出路径及最优参数输出路径
zonal_excel_result_path = r"D:\param_inversion\result\zonal_assessment"


#分区各工况下结果文件路径
zonal_result_calcu_path = r"D:\param_inversion\result\zonal_result_calcu"


#全局变量`
#分别存储不同区域结果的list
result_list_1=[]
result_list_2=[]
result_list_3=[]
result_list_4=[]
result_list_0=[]


#1生成粘聚力,内摩擦角，粘聚力的单位为：kPa,内摩擦角的单位为度
cohesion_range = range(13,17,1)
friction_range = range(1,30,1)
