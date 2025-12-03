#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试交互式模式启动
"""

import subprocess
import sys
import time

def test_interactive_mode():
    """
    测试交互式模式能否正常启动
    """
    print("测试交互式模式启动...")
    
    try:
        # 启动交互式模式，不使用text模式，手动处理编码
        process = subprocess.Popen(
            [sys.executable, "image_converter.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待程序启动并输出菜单
        time.sleep(1)
        
        # 读取输出，使用gbk编码（Windows默认编码）
        output_bytes = process.stdout.read(1024)
        
        # 尝试多种编码解码
        encodings = ['gbk', 'utf-8', 'utf-16']
        output = None
        for encoding in encodings:
            try:
                output = output_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if output is None:
            print("✗ 无法解码程序输出")
            return False
        
        # 检查是否显示了欢迎信息和菜单
        if "欢迎使用批量图片格式转换器" in output and "请选择操作" in output:
            print("✓ 交互式模式启动成功")
            print("✓ 菜单显示正常")
        else:
            print("✗ 交互式模式启动失败")
            print("输出内容:")
            print(output)
        
        # 发送退出命令，使用gbk编码
        process.stdin.write("2\n".encode('gbk'))
        process.stdin.flush()
        
        # 等待程序退出
        process.wait(timeout=2)
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_interactive_mode()