#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os

# 创建子目录
os.makedirs('test_input/subdir', exist_ok=True)

# 生成子目录测试图片
for i in range(2):
    img = Image.new('RGB', (100, 100), color=(i*100, 0, 0))
    img.save(f'test_input/subdir/subtest_{i}.png')

print("子目录测试图片生成完成！")