#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片格式转换器 - GUI版本
支持常见图片格式互转，如JPEG、PNG、BMP、GIF、TIFF等
"""

import os
import glob
import threading
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import Image

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("批量图片格式转换器")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # 设置全局字体
        self.root.option_add("*Font", "微软雅黑 10")
        
        # 初始化变量
        self.input_dir = StringVar()
        self.output_dir = StringVar(value="output")
        self.target_format = StringVar(value="jpg")
        self.quality = IntVar(value=85)
        self.recursive = BooleanVar(value=False)
        self.converting = False
        self.total_files = 0
        self.processed_files = 0
        
        # 创建主框架
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # 标题
        title_label = Label(main_frame, text="批量图片格式转换器", font=("微软雅黑", 14, "bold"))
        title_label.pack(pady=10)
        
        # 输入目录选择
        input_frame = Frame(main_frame)
        input_frame.pack(fill=X, pady=5)
        
        Label(input_frame, text="输入目录：").pack(side=LEFT)
        Entry(input_frame, textvariable=self.input_dir, width=30).pack(side=LEFT, padx=5, fill=X, expand=True)
        Button(input_frame, text="浏览", command=self.browse_input_dir).pack(side=LEFT, padx=5)
        
        # 输出目录选择
        output_frame = Frame(main_frame)
        output_frame.pack(fill=X, pady=5)
        
        Label(output_frame, text="输出目录：").pack(side=LEFT)
        Entry(output_frame, textvariable=self.output_dir, width=30).pack(side=LEFT, padx=5, fill=X, expand=True)
        Button(output_frame, text="浏览", command=self.browse_output_dir).pack(side=LEFT, padx=5)
        
        # 目标格式选择
        format_frame = Frame(main_frame)
        format_frame.pack(fill=X, pady=5)
        
        Label(format_frame, text="目标格式：").pack(side=LEFT)
        
        supported_formats = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif", "webp", "ico"]
        format_menu = ttk.Combobox(format_frame, textvariable=self.target_format, values=supported_formats, state="readonly", width=10)
        format_menu.pack(side=LEFT, padx=5)
        format_menu.current(0)
        
        # 质量设置
        quality_frame = Frame(main_frame)
        quality_frame.pack(fill=X, pady=5)
        
        Label(quality_frame, text="图片质量：").pack(side=LEFT)
        
        quality_scale = Scale(quality_frame, from_=0, to=100, orient=HORIZONTAL, variable=self.quality, length=200)
        quality_scale.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        self.quality_label = Label(quality_frame, text=f"{self.quality.get()}", width=4)
        self.quality_label.pack(side=LEFT, padx=5)
        
        # 递归选项
        recursive_frame = Frame(main_frame)
        recursive_frame.pack(fill=X, pady=5)
        
        Checkbutton(recursive_frame, text="递归处理子目录", variable=self.recursive).pack(side=LEFT)
        
        # 进度条
        self.progress_frame = Frame(main_frame)
        self.progress_frame.pack(fill=X, pady=15)
        
        self.progress_label = Label(self.progress_frame, text="准备就绪")
        self.progress_label.pack(side=LEFT)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack(side=LEFT, padx=10, fill=X, expand=True)
        
        # 状态信息
        self.status_frame = Frame(main_frame)
        self.status_frame.pack(fill=X, pady=5)
        
        self.status_label = Label(self.status_frame, text="", anchor=W)
        self.status_label.pack(fill=X)
        
        # 按钮区域
        button_frame = Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        self.start_button = Button(button_frame, text="开始转换", command=self.start_conversion, bg="#4CAF50", fg="white", height=2)
        self.start_button.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        self.stop_button = Button(button_frame, text="停止转换", command=self.stop_conversion, bg="#f44336", fg="white", height=2, state=DISABLED)
        self.stop_button.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        self.quit_button = Button(button_frame, text="退出", command=self.root.quit, bg="#2196F3", fg="white", height=2)
        self.quit_button.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        # 绑定事件
        self.quality.trace_add("write", self.update_quality_label)
        
    def update_quality_label(self, *args):
        """更新质量标签"""
        self.quality_label.config(text=f"{self.quality.get()}")
    
    def browse_input_dir(self):
        """浏览输入目录"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.input_dir.set(dir_path)
    
    def browse_output_dir(self):
        """浏览输出目录"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)
    
    def get_image_files(self, input_dir, recursive=False):
        """获取目录下所有图片文件"""
        # 支持的图片扩展名
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp", ".ico"]
        
        image_files = []
        
        if recursive:
            # 递归获取所有图片文件
            for root, _, files in os.walk(input_dir):
                for file in files:
                    if os.path.splitext(file)[1].lower() in image_extensions:
                        image_files.append(os.path.join(root, file))
        else:
            # 获取当前目录下所有图片文件
            for ext in image_extensions:
                image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext}"), recursive=False))
        
        return image_files
    
    def convert_image(self, img_path, output_dir, target_format, quality=85):
        """转换单张图片的格式"""
        try:
            # 打开图片
            with Image.open(img_path) as img:
                # 确保输出目录存在
                os.makedirs(output_dir, exist_ok=True)
                
                # 获取文件名（不含扩展名）
                filename = os.path.splitext(os.path.basename(img_path))[0]
                # 设置输出路径
                output_path = os.path.join(output_dir, f"{filename}.{target_format.lower()}")
                
                # 处理不同模式的图片
                if img.mode == "RGBA":
                    # RGBA模式转JPEG需要先转换为RGB
                    if target_format.lower() in ["jpg", "jpeg"]:
                        img = img.convert("RGB")
                elif img.mode == "P":
                    # 调色板模式转换
                    img = img.convert("RGB")
                
                # 转换格式并保存
                format_name = target_format.upper()
                if format_name == "JPG":
                    format_name = "JPEG"
                    
                save_params = {
                    "format": format_name,
                    "quality": quality
                }
                
                # 针对不同格式的特殊处理
                if target_format.lower() == "png":
                    save_params["optimize"] = True
                elif target_format.lower() in ["jpg", "jpeg"]:
                    save_params["optimize"] = True
                    save_params["subsampling"] = 0
                
                img.save(output_path, **save_params)
                
                return True, img_path, output_path, None
        except Exception as e:
            return False, img_path, None, str(e)
    
    def start_conversion(self):
        """开始转换（在新线程中执行）"""
        # 验证输入
        if not self.input_dir.get():
            messagebox.showerror("错误", "请选择输入目录")
            return
        
        if not os.path.isdir(self.input_dir.get()):
            messagebox.showerror("错误", f"目录 '{self.input_dir.get()}' 不存在")
            return
        
        # 获取图片文件
        image_files = self.get_image_files(self.input_dir.get(), self.recursive.get())
        if not image_files:
            messagebox.showinfo("提示", "未找到图片文件")
            return
        
        # 更新UI状态
        self.converting = True
        self.total_files = len(image_files)
        self.processed_files = 0
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.progress_bar.config(value=0, maximum=self.total_files)
        self.progress_label.config(text="0/0")
        self.status_label.config(text=f"找到 {self.total_files} 张图片，准备开始转换...")
        
        # 在新线程中执行转换
        conversion_thread = threading.Thread(
            target=self.convert_batch,
            args=(image_files,)
        )
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def convert_batch(self, image_files):
        """批量转换图片"""
        success_count = 0
        fail_count = 0
        fail_list = []
        
        for img_path in image_files:
            if not self.converting:
                break
            
            success, input_path, output_path, error = self.convert_image(
                img_path, 
                self.output_dir.get(), 
                self.target_format.get(), 
                self.quality.get()
            )
            
            self.processed_files += 1
            
            if success:
                success_count += 1
            else:
                fail_count += 1
                fail_list.append((input_path, error))
            
            # 更新UI
            self.root.after(0, self.update_progress, success_count, fail_count)
        
        # 转换完成
        self.root.after(0, self.conversion_finished, success_count, fail_count, fail_list)
    
    def update_progress(self, success_count, fail_count):
        """更新进度"""
        self.progress_bar.config(value=self.processed_files)
        self.progress_label.config(text=f"{self.processed_files}/{self.total_files}")
        self.status_label.config(text=f"已转换 {self.processed_files}/{self.total_files} 张，成功 {success_count} 张，失败 {fail_count} 张")
    
    def conversion_finished(self, success_count, fail_count, fail_list):
        """转换完成处理"""
        self.converting = False
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        
        if self.processed_files == 0:
            self.progress_label.config(text="转换已取消")
            self.status_label.config(text="转换已取消")
            messagebox.showinfo("提示", "转换已取消")
        else:
            self.progress_label.config(text="转换完成")
            self.status_label.config(text=f"转换完成：成功 {success_count} 张，失败 {fail_count} 张")
            
            # 显示结果
            result_msg = f"转换完成！\n\n成功：{success_count} 张\n失败：{fail_count} 张\n\n输出目录：{os.path.abspath(self.output_dir.get())}"
            
            if fail_list:
                result_msg += f"\n\n失败列表（显示前5个）："
                for i, (img_path, error) in enumerate(fail_list[:5]):
                    result_msg += f"\n{i+1}. {os.path.basename(img_path)}: {error[:50]}..."
                if len(fail_list) > 5:
                    result_msg += f"\n... 还有 {len(fail_list) - 5} 个失败项"
            
            messagebox.showinfo("转换完成", result_msg)
    
    def stop_conversion(self):
        """停止转换"""
        if messagebox.askyesno("确认", "确定要停止转换吗？"):
            self.converting = False

if __name__ == "__main__":
    root = Tk()
    app = ImageConverterGUI(root)
    root.mainloop()