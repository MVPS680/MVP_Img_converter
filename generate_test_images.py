#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os

# 创建测试目录
os.makedirs('test_input', exist_ok=True)

# 生成测试图片
for i in range(3):
    # 创建不同颜色的测试图片
    img = Image.new('RGB', (100, 100), color=(i*50, i*50, i*50))
    # 保存为PNG格式
    img.save(f'test_input/test_{i}.png')
    # 保存为JPG格式
    img.save(f'test_input/test_{i}.jpg')

print("测试图片生成完成！")