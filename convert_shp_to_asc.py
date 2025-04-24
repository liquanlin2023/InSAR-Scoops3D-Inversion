import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np
from config import dem_asc_file, slow_moving_landslide_shp_flie_path, slow_moving_landslide_asc_file
import warnings

# 过滤特定的警告信息
warnings.filterwarnings("ignore", category=UserWarning, module='rasterio')

# DEM 文件的 CRS
DEM_CRS = 'EPSG:32648'  # UTM 48N 的 EPSG 代码

def convert_shp_to_asc(shp_file, output_asc_file):
    """
    接收shp文件，按照dem.asc头文件格式将其转换为相应的asc文件，
    :param shp_file: shp文件路径
    :param output_asc_file: 输出asc文件路径
    :return: none
    """
    # 读取shapefile
    gdf = gpd.read_file(shp_file)

    # 读取DEM ASC文件以获取模板和头部信息
    with open(dem_asc_file, 'r') as dem_file:
        header_lines = [next(dem_file) for _ in range(6)]

    # 解析头部信息的值
    ncols = int(header_lines[0].split()[1])
    nrows = int(header_lines[1].split()[1])
    xllcorner = float(header_lines[2].split()[1])
    yllcorner = float(header_lines[3].split()[1])
    cellsize = float(header_lines[4].split()[1])
    nodata_value = int(header_lines[5].split()[1])

    # 读取DEM ASC文件以获取栅格化的模板
    with rasterio.open(dem_asc_file) as dem_src:
        dem_data = dem_src.read(1)
        transform = dem_src.transform
        dem_crs = dem_src.crs if dem_src.crs else DEM_CRS

    # 检查 Shapefile 的 CRS，如果不同，则进行重投影
    if gdf.crs != dem_crs:
        gdf = gdf.to_crs(dem_crs)

    # 将shapefile的几何图形栅格化，以匹配DEM模板
    shapes = ((geom, 1) for geom in gdf.geometry)
    rasterized = rasterize(
        shapes,
        out_shape=dem_data.shape,
        transform=transform,
        fill=nodata_value,  # 使用与DEM相同的nodata值
        dtype=np.int32  # 确保数据类型正确
    )

    # 确保在栅格化数据中正确设置nodata值
    rasterized = np.where(rasterized == 0, nodata_value, rasterized)

    # 使用与DEM ASC文件完全相同的头部写入ASC文件
    with open(output_asc_file, 'w') as asc_file:
        asc_file.writelines(header_lines)  # 写入复制的头部信息

        # 写入栅格化的数据
        np.savetxt(asc_file, rasterized, fmt='%d')


