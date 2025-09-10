#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    """
    读取数据文件并返回时间和对应的值
    
    Parameters:
    -----------
    filename : str
        输入文件名
    
    Returns:
    --------
    time_ns : numpy.ndarray
        时间数据（ns）
    values : numpy.ndarray
        对应的数值
    """
    data = np.loadtxt(filename, skiprows=1)
    return data[:, 0], data[:, 1]

def read_rmsf(filename):
    """
    读取RMSF数据文件
    
    Parameters:
    -----------
    filename : str
        RMSF数据文件名
    
    Returns:
    --------
    residues : numpy.ndarray
        残基序号
    rmsf_values : numpy.ndarray
        RMSF值
    """
    data = np.loadtxt(filename, skiprows=1)
    return data[:, 0], data[:, 1]

def plot_comparison(time1, values1, time2, values2, output_file, ylabel, title=None, ylim=None):
    """
    绘制时间序列对比图
    
    Parameters:
    -----------
    time1 : numpy.ndarray
        第一个数据集的时间数据
    values1 : numpy.ndarray
        第一个数据集的数值
    time2 : numpy.ndarray
        第二个数据集的时间数据
    values2 : numpy.ndarray
        第二个数据集的数值
    output_file : str
        输出文件名
    ylabel : str
        y轴标签
    title : str, optional
        图表标题
    ylim : tuple, optional
        y轴范围 (ymin, ymax)
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(time1, values1, linestyle='-', color='green')
    plt.plot(time2, values2, linestyle='-', color='purple')
    
    plt.xlabel('Time (ns)', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    if title:
        plt.title(title, fontsize=16)
    
    # 设置y轴范围
    if ylim:
        plt.ylim(ylim)
    
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"对比图已保存为: {output_file}")


def plot_rmsf_comparison(residues1, values1, residues2, values2, output_file):
    """
    绘制RMSF对比图
    
    Parameters:
    -----------
    residues1 : numpy.ndarray
        第一个数据集的残基序号
    values1 : numpy.ndarray
        第一个数据集的RMSF值
    residues2 : numpy.ndarray
        第二个数据集的残基序号
    values2 : numpy.ndarray
        第二个数据集的RMSF值
    output_file : str
        输出文件名
    """
    plt.figure(figsize=(12, 6))
    
    plt.plot(residues1, values1, linestyle='-', color='green')
    plt.plot(residues2, values2, linestyle='-', color='purple')
    
    plt.xlabel('Residue Index', fontsize=14)
    plt.ylabel('RMSF (Å)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"RMSF对比图已保存为: {output_file}")



def main():
    # 基础路径
    base_path1 = '/home/xxx/MD_20250330/PLpro/3d_pdbqt/7mc9_single/cpptraj'
    base_path2 = '/home/xxx/MD_20250330/PLpro/3d_pdbqt/SH144_md/cpptarj'
  
    
    # 读取SASA数据
    time1, sasa1 = read_data(f'{base_path1}/sasa_ns.dat')
    time2, sasa2 = read_data(f'{base_path2}/sasa_ns.dat')
    plot_comparison(time1, sasa1, time2, sasa2, 'SASA_7mc9_SH144.png', 'SASA (Å²)', ylim=(8000, 16000))
    
    # 读取RMSD数据
    time1, rmsd1 = read_data(f'{base_path1}/rmsd_ns.dat')
    time2, rmsd2 = read_data(f'{base_path2}/rmsd_ns.dat')
    plot_comparison(time1, rmsd1, time2, rmsd2, 'RMSD_7mc9_SH144.png', 'RMSD (Å)')
    
    # 读取RoG数据
    time1, rog1 = read_data(f'{base_path1}/RoG_ns.dat')
    time2, rog2 = read_data(f'{base_path2}/RoG_ns.dat')
    plot_comparison(time1, rog1, time2, rog2, 'RoG_7mc9_SH144.png', 'Radius of Gyration (Å)', ylim=(17, 21))
    
    # 读取RMSF数据
    residues1, rmsf1 = read_rmsf(f'{base_path1}/rmsf.dat')
    residues2, rmsf2 = read_rmsf(f'{base_path2}/rmsf.dat')
    plot_rmsf_comparison(residues1, rmsf1, residues2, rmsf2, 'RMSF_7mc9_SH144.png')

if __name__ == "__main__":
    main()







