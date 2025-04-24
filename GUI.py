import tkinter as tk
from tkinter import filedialog
import configparser
from PIL import Image, ImageTk

class ParameterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("参数输入界面")

        # 设置背景图片
        # self.set_background("background.png")  # 确保背景图片文件路径正确

        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')

        # 创建输入框和标签
        self.entries = {}
        self.create_entry("scoops3d输入文件:", 'scoops3d_param_file_path', self.browse_scoops3d_param)
        self.create_entry("高程文件:", 'dem_asc_file', self.browse_dem_asc)
        self.create_entry("scoop3d执行文件:", 'scoops3d_exe_file_path', self.browse_scoops3d_exe)
        self.create_entry("insar滑坡shp文件:", 'slow_moving_landslide_shp_flie_path', self.browse_landslide_shp)
        self.create_entry("历史滑坡:", 'landslide', self.browse_landslide)
        self.create_entry("滑坡asc路径:", 'slow_moving_landslide_asc_file', self.browse_landslide_asc)
        self.create_entry("岩组分区栅格:", 'zones_file_path', self.browse_zones)
        self.create_entry("分区岩土材料参数文件路径预设置:", 'material_file_path', self.browse_material)
        self.create_entry("结果输出路径:", 'directory', self.browse_directory)
        self.create_entry("分区评估表格输出路径及最优参数输出路径:", 'zonal_excel_result_path', self.browse_zonal_excel)
        self.create_entry("分区各工况下结果文件路径:", 'zonal_result_calcu_path', self.browse_zonal_result)

        self.create_button("保存参数", self.save_config)

    def set_background(self, image_path):
        self.background_image = Image.open(image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

    def create_entry(self, label_text, config_key, browse_command):
        frame = tk.Frame(self.root, bg="#f0f0f0")  # 设置背景颜色，以确保标签和输入框可见
        frame.pack(pady=5, fill='x')
        label = tk.Label(frame, text=label_text, width=40, anchor='w', bg="#f0f0f0")  # 设置背景颜色
        label.pack(side="left")
        entry = tk.Entry(frame, width=50)
        entry.insert(0, self.config.get('DEFAULT', config_key, fallback=''))
        entry.pack(side="left", padx=(0, 5))
        button = tk.Button(frame, text="浏览", command=browse_command)
        button.pack(side="left")
        self.entries[config_key] = entry

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=5)

    def browse_scoops3d_param(self):
        file_path = filedialog.askopenfilename(title="选择scoops3d输入文件",
                                               filetypes=(("Scoops3D参数文件", "*.scp"), ("所有文件", "*.*")))
        if file_path:
            self.entries['scoops3d_param_file_path'].delete(0, tk.END)
            self.entries['scoops3d_param_file_path'].insert(0, file_path)

    def browse_dem_asc(self):
        file_path = filedialog.askopenfilename(title="选择高程文件",
                                               filetypes=(("ASC文件", "*.asc"), ("所有文件", "*.*")))
        if file_path:
            self.entries['dem_asc_file'].delete(0, tk.END)
            self.entries['dem_asc_file'].insert(0, file_path)

    def browse_scoops3d_exe(self):
        file_path = filedialog.askopenfilename(title="选择scoop3d执行文件",
                                               filetypes=(("可执行文件", "*.exe"), ("所有文件", "*.*")))
        if file_path:
            self.entries['scoops3d_exe_file_path'].delete(0, tk.END)
            self.entries['scoops3d_exe_file_path'].insert(0, file_path)

    def browse_landslide_shp(self):
        file_path = filedialog.askopenfilename(title="选择insar滑坡shp文件",
                                               filetypes=(("Shapefile", "*.shp"), ("所有文件", "*.*")))
        if file_path:
            self.entries['slow_moving_landslide_shp_flie_path'].delete(0, tk.END)
            self.entries['slow_moving_landslide_shp_flie_path'].insert(0, file_path)

    def browse_landslide(self):
        file_path = filedialog.askopenfilename(title="选择历史滑坡文件",
                                               filetypes=(("Shapefile", "*.shp"), ("所有文件", "*.*")))
        if file_path:
            self.entries['landslide'].delete(0, tk.END)
            self.entries['landslide'].insert(0, file_path)

    def browse_landslide_asc(self):
        file_path = filedialog.askopenfilename(title="选择滑坡asc路径",
                                               filetypes=(("ASC文件", "*.asc"), ("所有文件", "*.*")))
        if file_path:
            self.entries['slow_moving_landslide_asc_file'].delete(0, tk.END)
            self.entries['slow_moving_landslide_asc_file'].insert(0, file_path)

    def browse_zones(self):
        file_path = filedialog.askopenfilename(title="选择岩组分区栅格",
                                               filetypes=(("ASC文件", "*.asc"), ("所有文件", "*.*")))
        if file_path:
            self.entries['zones_file_path'].delete(0, tk.END)
            self.entries['zones_file_path'].insert(0, file_path)

    def browse_material(self):
        file_path = filedialog.askopenfilename(title="选择分区岩土材料参数文件",
                                               filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*")))
        if file_path:
            self.entries['material_file_path'].delete(0, tk.END)
            self.entries['material_file_path'].insert(0, file_path)

    def browse_directory(self):
        file_path = filedialog.askdirectory(title="选择结果输出路径")
        if file_path:
            self.entries['directory'].delete(0, tk.END)
            self.entries['directory'].insert(0, file_path)

    def browse_zonal_excel(self):
        file_path = filedialog.askdirectory(title="选择分区评估表格输出路径")
        if file_path:
            self.entries['zonal_excel_result_path'].delete(0, tk.END)
            self.entries['zonal_excel_result_path'].insert(0, file_path)

    def browse_zonal_result(self):
        file_path = filedialog.askdirectory(title="选择分区各工况下结果文件路径")
        if file_path:
            self.entries['zonal_result_calcu_path'].delete(0, tk.END)
            self.entries['zonal_result_calcu_path'].insert(0, file_path)

    def save_config(self):
        for key, entry in self.entries.items():
            self.config.set('DEFAULT', key, entry.get())

        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        print("参数已保存到 config.ini 文件中")

