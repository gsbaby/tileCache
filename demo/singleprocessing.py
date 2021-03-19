import gdal2tiles
import os


# #设置需要切图的级别，设置恢复模式，显示生成切片的输出
# options = {‘zoom’: (11, 12), ‘resume’: True,‘verbose’:True}
# gdal2tiles.generate_tiles(‘输入的影像文件’,
# ‘输出的切片文件夹’, **options)

def gdal_generate_tiles(input_file, output_dir, option):
    # 参数：
    # input_file （str）：输入文件的路径。
    # output_folder （str）：输出文件夹的路径。
    # options：图块生成选项。
    gdal2tiles.generate_tiles(input_file, output_dir, **option)


if __name__ == '__main__':
    input_file = './Test/input/WH_BT_DEM_12_5.tif'
    # input_file = './Test/input/FuYangShi_Download_WGS84.shp'   #shp不支持
    output_file_dir = './Test/output/WH_BT_DEM_12_5'
    if not os.path.exists(output_file_dir):
        os.mkdir(output_file_dir)
    option = {
        'zoom': (10, 21),
        'resume': True,
        'verbose': True,
        'nb_processes': 4
    }
    ###
    # https://gdal2tiles.readthedocs.io/en/latest/gdal2tiles.html#module-gdal2tiles.gdal2tiles
    # profile (str): Tile cutting profile (mercator,geodetic,raster) - default‘mercator’ (Google Maps compatible)
    # resampling(str): Resampling method(average, near, bilinear, cubic, cubicsp line, lanczos, antialias) - default ‘average’
    # s_srs: The spatial reference system used for the source input data
    ###
    gdal_generate_tiles(input_file, output_file_dir, option)
