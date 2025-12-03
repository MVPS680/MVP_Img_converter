#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片格式转换器
支持常见图片格式互转，如JPEG、PNG、BMP、GIF、TIFF等
"""

import os
import glob
import argparse
import sys
from PIL import Image
from tqdm import tqdm

def convert_image(img_path, output_dir, target_format, quality=85):
    """
    转换单张图片的格式
    
    Args:
        img_path: 输入图片路径
        output_dir: 输出目录路径
        target_format: 目标格式（如jpg、png等）
        quality: 输出图片质量（0-100）
        
    Returns:
        tuple: (是否成功, 输入路径, 输出路径, 错误信息)
    """
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
            # 处理JPG格式名称映射
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

def get_image_files(input_dir, recursive=False):
    """
    获取目录下所有图片文件
    
    Args:
        input_dir: 输入目录
        recursive: 是否递归处理子目录
        
    Returns:
        list: 图片文件路径列表
    """
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

def interactive_mode():
    """
    交互式模式
    """
    print("=" * 50)
    print("欢迎使用批量图片格式转换器")
    print("=" * 50)
    print("使用方法：")
    print("第一步：把要处理的任意格式的图片都放在一个文件夹里，并复制文件夹的路径")
    print("第二步：输入1开始转换")
    print("第三步：根据指示完成转换\n")
    print("享受！")
    print('-' * 50)
    print('作者：MVP')
    print('=' * 50)    
    
    while True:
        # 显示菜单
        print("\n请选择操作：")
        print("1. 批量转换图片格式")
        print("2. 退出程序")
        
        # 获取用户选择
        choice = input("\n请输入选项编号 (1-2): ").strip()
        
        if choice == "1":
            # 批量转换图片格式
            print("\n" + "-" * 30)
            print("批量转换图片格式")
            print("-" * 30)
            
            # 获取输入目录
            input_dir = input("请输入图片所在目录（文件夹）路径: ").strip()
            while not os.path.isdir(input_dir):
                print(f"错误：目录 '{input_dir}' 不存在，请重新输入")
                input_dir = input("请输入图片所在目录路径: ").strip()
            
            # 获取输出目录
            output_dir = input("请输入输出目录路径 (默认: output): ").strip()
            if not output_dir:
                output_dir = "output"
            
            # 获取目标格式
            supported_formats = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif", "webp", "ico"]
            target_format = input(f"请输入目标格式 ({'/'.join(supported_formats)}): ").strip().lower()
            while target_format not in supported_formats:
                print(f"错误：不支持的格式 '{target_format}'，请从支持的格式中选择")
                target_format = input(f"请输入目标格式 ({'/'.join(supported_formats)}): ").strip().lower()
            
            # 获取递归选项
            recursive = input("是否递归处理子目录？(y/n，默认: n): ").strip().lower()
            recursive = recursive == "y"
            
            # 获取质量参数
            quality = input("请输入图片质量 (0-100，默认: 85): ").strip()
            if not quality:
                quality = 85
            else:
                try:
                    quality = int(quality)
                    if quality < 0 or quality > 100:
                        print("警告：质量参数超出范围，使用默认值 85")
                        quality = 85
                except ValueError:
                    print("警告：无效的质量参数，使用默认值 85")
                    quality = 85
            
            # 确认参数
            print("\n" + "-" * 30)
            print("转换参数确认")
            print("-" * 30)
            print(f"输入目录: {input_dir}")
            print(f"输出目录: {output_dir}")
            print(f"目标格式: {target_format}")
            print(f"递归处理: {'是' if recursive else '否'}")
            print(f"图片质量: {quality}")
            
            confirm = input("\n是否开始转换？(y/n): ").strip().lower()
            if confirm != "y":
                print("\n转换已取消")
                continue
            
            # 执行转换
            print(f"\n正在扫描图片文件...")
            image_files = get_image_files(input_dir, recursive)
            
            if not image_files:
                print(f"未找到图片文件")
                continue
            
            print(f"找到 {len(image_files)} 张图片")
            print(f"开始转换为 {target_format.upper()} 格式...")
            
            success_count = 0
            fail_count = 0
            fail_list = []
            
            # 使用tqdm显示进度
            for img_path in tqdm(image_files, desc="转换进度"):
                success, input_path, output_path, error = convert_image(
                    img_path, output_dir, target_format, quality
                )
                
                if success:
                    success_count += 1
                else:
                    fail_count += 1
                    fail_list.append((input_path, error))
            
            # 输出转换结果
            print("\n" + "=" * 30)
            print("转换完成！")
            print("=" * 30)
            print(f"成功：{success_count} 张")
            print(f"失败：{fail_count} 张")
            
            if fail_list:
                print("\n失败列表：")
                for img_path, error in fail_list:
                    print(f"  {img_path}: {error}")
            
            print(f"\n输出目录：{os.path.abspath(output_dir)}")
            print("\n" + "=" * 30)
            
            # 询问是否继续
            continue_choice = input("是否继续其他操作？(y/n，默认: y): ").strip().lower()
            if continue_choice != "y":
                print("\n感谢使用，再见！")
                break
        
        elif choice == "2":
            # 退出程序
            print("\n感谢使用，再见！")
            break
        
        else:
            # 无效选项
            print(f"错误：无效的选项 '{choice}'，请输入 1 或 2")


def main():
    """
    主函数
    """
    # 判断是否使用命令行参数
    if len(sys.argv) > 1:
        # 命令行模式
        parser = argparse.ArgumentParser(description="批量图片格式转换器")
        parser.add_argument("-i", "--input", required=True, help="输入目录路径")
        parser.add_argument("-o", "--output", default="output", help="输出目录路径，默认创建output目录")
        parser.add_argument("-f", "--format", required=True, help="目标格式，如jpg、png等")
        parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
        parser.add_argument("-q", "--quality", type=int, default=85, help="输出图片质量（0-100），默认85")
        
        args = parser.parse_args()
        
        # 验证输入目录是否存在
        if not os.path.isdir(args.input):
            print(f"错误：输入目录 '{args.input}' 不存在")
            return
        
        # 验证输出质量参数
        if args.quality < 0 or args.quality > 100:
            print(f"错误：输出质量必须在0-100之间，当前值为 {args.quality}")
            return
        
        # 获取所有图片文件
        print(f"正在扫描图片文件...")
        image_files = get_image_files(args.input, args.recursive)
        
        if not image_files:
            print(f"未找到图片文件")
            return
        
        print(f"找到 {len(image_files)} 张图片")
        
        # 开始转换
        print(f"开始转换为 {args.format.upper()} 格式...")
        
        success_count = 0
        fail_count = 0
        fail_list = []
        
        # 使用tqdm显示进度
        for img_path in tqdm(image_files, desc="转换进度"):
            success, input_path, output_path, error = convert_image(
                img_path, args.output, args.format, args.quality
            )
            
            if success:
                success_count += 1
            else:
                fail_count += 1
                fail_list.append((input_path, error))
        
        # 输出转换结果
        print("\n转换完成！")
        print(f"成功：{success_count} 张")
        print(f"失败：{fail_count} 张")
        
        if fail_list:
            print("\n失败列表：")
            for img_path, error in fail_list:
                print(f"  {img_path}: {error}")
        
        print(f"\n输出目录：{os.path.abspath(args.output)}")
    else:
        # 交互式模式
        interactive_mode()

if __name__ == "__main__":
    main()