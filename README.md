# 批量图片格式转换器

一个简单易用的Python批量图片格式转换工具，支持常见图片格式之间的相互转换，提供命令行和图形界面两种使用方式。

## 功能特性

- 支持多种图片格式：JPEG、PNG、BMP、GIF、TIFF、WebP、ICO
- 批量处理：一次性转换整个目录中的所有图片
- 递归处理：可选择是否处理子目录中的图片
- 质量控制：可调整输出图片的质量（0-100）
- 两种使用方式：命令行模式和图形界面模式
- 进度显示：实时显示转换进度和结果统计

## 环境要求

- Python 3.6+
- 依赖库：
  - Pillow（用于图片处理）
  - tqdm（用于显示进度条）

## 安装依赖

```bash
pip install pillow tqdm
```

## 使用方法

### 方式一：命令行模式

直接运行程序进入交互式模式：

```bash
python image_converter.py
```

按照提示输入：
1. 选择操作（批量转换图片格式或退出）
2. 输入图片所在目录路径
3. 输入输出目录路径（默认为output）
4. 选择目标格式
5. 选择是否递归处理子目录
6. 输入图片质量（0-100，默认85）

或者使用命令行参数直接执行：

```bash
python image_converter.py -i 输入目录 -o 输出目录 -f 目标格式 [-r] [-q 质量]
```

参数说明：
- `-i, --input`：输入目录路径（必需）
- `-o, --output`：输出目录路径（可选，默认为output）
- `-f, --format`：目标格式（必需）
- `-r, --recursive`：递归处理子目录（可选）
- `-q, --quality`：输出图片质量0-100（可选，默认85）

示例：

```bash
# 将当前目录下的所有图片转换为PNG格式
python image_converter.py -i . -o output -f png

# 递归处理子目录，转换为JPG格式，质量90
python image_converter.py -i input_folder -o output_folder -f jpg -r -q 90
```

### 方式二：图形界面模式

运行GUI版本：

```bash
python Guiversion/image_converter_gui.py
```

使用图形界面的步骤：
1. 点击"浏览"按钮选择输入目录
2. 选择或输入输出目录
3. 从下拉菜单选择目标格式
4. 调整图片质量滑块
5. 勾选"递归处理子目录"（如需要）
6. 点击"开始转换"按钮
7. 查看进度条和状态信息
8. 转换完成后查看结果

## 核心实现原理

### 1. 图片格式转换

程序使用Pillow库来处理图片格式转换。核心转换逻辑如下：

```python
from PIL import Image

def convert_image(img_path, output_dir, target_format, quality=85):
    """转换单张图片的格式"""
    # 打开图片文件
    with Image.open(img_path) as img:
        # 处理特殊颜色模式
        # RGBA模式（带透明通道）转JPEG时需要先转为RGB
        if img.mode == "RGBA" and target_format.lower() in ["jpg", "jpeg"]:
            img = img.convert("RGB")
        # 调色板模式转换为RGB
        elif img.mode == "P":
            img = img.convert("RGB")
        
        # 根据格式设置保存参数
        save_params = {
            "format": target_format.upper(),
            "quality": quality
        }
        
        # PNG格式启用优化
        if target_format.lower() == "png":
            save_params["optimize"] = True
        # JPEG格式启用优化并设置子采样
        elif target_format.lower() in ["jpg", "jpeg"]:
            save_params["optimize"] = True
            save_params["subsampling"] = 0
        
        # 保存转换后的图片
        output_path = os.path.join(output_dir, f"{filename}.{target_format.lower()}")
        img.save(output_path, **save_params)
```

### 2. 批量文件获取

程序支持两种模式获取图片文件：

```python
import os
import glob

def get_image_files(input_dir, recursive=False):
    """获取目录下所有图片文件"""
    # 支持的图片扩展名列表
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp", ".ico"]
    
    if recursive:
        # 递归模式：遍历所有子目录
        for root, _, files in os.walk(input_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    image_files.append(os.path.join(root, file))
    else:
        # 非递归模式：只获取当前目录
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext}")))
    
    return image_files
```

### 3. GUI多线程处理

图形界面版本使用多线程避免界面卡顿：

```python
import threading

class ImageConverterGUI:
    def start_conversion(self):
        """开始转换（在新线程中执行）"""
        # 创建转换线程
        conversion_thread = threading.Thread(
            target=self.convert_batch,
            args=(image_files,)
        )
        # 设置为守护线程，主程序退出时自动结束
        conversion_thread.daemon = True
        # 启动线程
        conversion_thread.start()
    
    def convert_batch(self, image_files):
        """在后台线程中执行批量转换"""
        for img_path in image_files:
            # 执行转换逻辑
            success = self.convert_image(img_path, ...)
            
            # 使用after方法在主线程更新UI
            self.root.after(0, self.update_progress, success_count, fail_count)
```

## 测试

项目提供了测试图片生成脚本：

```bash
# 生成基础测试图片（在test_input目录中）
python generate_test_images.py

# 生成子目录测试图片
python generate_subdir_images.py
```

## 支持的格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff, .tif)
- WebP (.webp)
- ICO (.ico)

## 注意事项

1. RGBA模式（带透明通道）的图片转换为JPEG格式时，透明通道会被丢弃
2. 转换质量参数仅对有损格式（如JPEG、WebP）有效
3. 输出目录如果不存在会自动创建
4. GUI版本使用多线程处理，转换过程中可以随时停止
5. 源图片不会被修改，所有转换后的图片都会保存到输出目录

## 项目结构

```
图片处理器/
├── image_converter.py              # 命令行版本主程序
├── Guiversion/
│   └── image_converter_gui.py      # 图形界面版本
├── generate_test_images.py         # 测试图片生成脚本
├── generate_subdir_images.py       # 子目录测试图片生成脚本
├── test_input/                     # 测试图片目录
│   ├── test_0.jpg
│   ├── test_0.png
│   └── subdir/
│       └── subtest_0.png
└── README.md                       # 项目说明文档
```

## 许可证

本项目采用开源许可证，详见LICENSE文件。