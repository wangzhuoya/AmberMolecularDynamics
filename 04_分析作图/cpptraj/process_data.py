#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def process_file(input_file):
    """
    处理数据文件：
    1. 将第一列名从Frame改为Time(ns)
    2. 将第一列数值乘以0.01（每帧间隔为10ps）
    3. 保存为新文件
    """
    # 读取输入文件
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # 生成输出文件名
    output_file = input_file.replace('.dat', '_ns.dat')
    
    # 处理并写入新文件
    with open(output_file, 'w') as out:
        for line in lines:
            # 跳过以'#'开头的标题行
            if line.startswith('#'):
                continue
            # 分割每行的数据
            columns = line.split()
            if len(columns) >= 2:  # 确保至少有两列数据
                # 将第一列由frame转换为time (t=i*ntwx*dt=i*10ps=i*0.01ns)
                first_column = float(columns[0]) * 0.01
                # 保留第二列数据
                second_column = float(columns[1])
                # 写入新文件
                out.write(f"{first_column:.6f}    {second_column}\n")
    
    print(f"已处理文件: {input_file} -> {output_file}")

def main():
    # 要处理的文件列表
    files = [
        "rmsd.dat",
        "RoG.dat",
        "sasa.dat"
    ]
    
    # 处理每个文件
    for file in files:
        if os.path.exists(file):
            process_file(file)
        else:
            print(f"警告: 文件不存在 - {file}")

if __name__ == "__main__":
    main() 
