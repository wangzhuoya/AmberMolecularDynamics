#!/bin/bash

# --- AMBER 环境配置 ---
# amber20
# 加载 AMBER 20 的环境变量和路径设置，使得系统能找到 pmemd.cuda 等程序。
source /home/xxx/software/amber20/amber.sh



# --- GPU 环境配置 ---
# 将 pmemd.cuda 程序能“看到”的 GPU 设备限制为第一块卡 (编号为 0)。
# 这是一个非常重要的步骤，用于在多 GPU 服务器上指定使用哪一块 GPU 进行计算。
export CUDA_VISIBLE_DEVICES="0"


# ----------- 分子动力学模拟流程 -----------

# 第1步：能量最小化 (第一阶段 - 约束骨架)
# 消除初始结构中不合理的接触（如原子重叠），为后续模拟做准备。
# -O: 覆盖已存在的输出文件。
# -i min1.in: 指定输入参数文件，其中定义了最小化的算法和参数，以及对分子骨架施加约束。
# -o rec_ions_min1.out: 指定输出日志文件名。
# -p rec_ions.prmtop: 指定拓扑文件，描述了分子的连接、原子类型和力场参数。
# -c rec_ions.inpcrd: 指定初始坐标文件。
# -r rec_ions_min1.rst: 指定输出的重启文件，包含了最小化后的坐标，将作为下一步的输入。
# -ref rec_ions.inpcrd: 指定用于计算位置约束的参考坐标文件。
pmemd.cuda -O -i min1.in -o rec_ions_min1.out -p rec_ions.prmtop -c rec_ions.inpcrd -r rec_ions_min1.rst -ref rec_ions.inpcrd

# 第2步：能量最小化 (第二阶段 - 无约束)
# 在释放了对骨架的约束后，对整个系统进行进一步的能量最小化，让系统完全弛豫。
# -c rec_ions_min1.rst: 使用上一步输出的重启文件作为输入坐标。
# -r rec_ions_min2.rst: 指定本步骤的输出重启文件。
pmemd.cuda -O -i min2.in -o rec_ions_min2.out -p rec_ions.prmtop -c rec_ions_min1.rst -r rec_ions_min2.rst

# 第3步：加热 (NVT系综)
# 在保持系统体积不变 (NVT系综) 的情况下，将系统缓慢地从低温（例如 0 K 或 100 K）加热到目标温度（例如 300 K）。
# -i heat.in: 指定加热过程的输入参数（如目标温度、时间步长等）。
# -x rec_ions_heat.nc: 指定输出的轨迹文件名 (NetCDF格式)，记录了原子随时间变化的坐标。
# -ref rec_ions_min2.rst: 指定用于位置约束的参考结构。
pmemd.cuda -O -i heat.in -o rec_ions_heat.out -p rec_ions.prmtop -c rec_ions_min2.rst -r rec_ions_heat.rst  -x rec_ions_heat.nc -ref rec_ions_min2.rst

# 第4步：平衡 (第一阶段 - NPT系综)
# 在保持系统温度和压强不变 (NPT系综) 的情况下，让系统的密度达到平衡。
# -i press.in: 指定该平衡阶段的输入参数（如目标压强、控压方法等）。
# -c rec_ions_heat.rst: 使用加热步骤结束时的状态作为输入。
pmemd.cuda -O -i press.in -o rec_ions_press.out -p rec_ions.prmtop -c rec_ions_heat.rst -r rec_ions_press.rst -x rec_ions_press.nc -ref rec_ions_min2.rst

# 第5步：平衡 (第二阶段 - NPT系综，时长 10ns)
# 在恒温恒压下进行一个较长时间的平衡模拟（这里是 10 纳秒），确保系统各方面性质（如能量、密度、RMSD等）都达到稳定。
# -i eq.in: 指定该平衡阶段的输入参数。
pmemd.cuda -O -i eq.in -o rec_ions_eq.out -p rec_ions.prmtop -c rec_ions_press.rst -r rec_ions_eq.rst -x rec_ions_eq.nc

# 第6步：成品模拟 (Production MD，时长 100ns)
# -i md.in: 指定生产模拟的输入参数。
pmemd.cuda -O -i md.in -o rec_ions_md.out -p rec_ions.prmtop -c rec_ions_eq.rst -r rec_ions_md.rst -x rec_ions_md.nc
