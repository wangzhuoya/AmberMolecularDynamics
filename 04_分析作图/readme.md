# 使用CPPTRAJ进行AMBER分子动力学轨迹分析与可视化

本文档详细介绍如何使用 AmberTools 中的 `CPPTRAJ` 程序对分子动力学（MD）模拟轨迹进行分析，并结合 Python（Matplotlib/Numpy）进行数据处理和科学绘图。

## 1. CPPTRAJ 简介

`CPPTRAJ` 是 AMBER 套件中用于处理坐标轨迹和数据文件的核心工具，是其前身 PTRAJ 的一个功能更强大、性能更优越的重写版本。它支持并行计算（OpenMP & MPI），能处理多种压缩格式的轨迹文件，并提供了丰富的轨迹分析和处理选项。

**基本输入文件**:
*   **拓扑文件 (`.prmtop`)**: 定义了系统的分子结构、连接性和力场参数。
*   **轨迹文件 (`.nc`)**: 记录了模拟过程中原子坐标随时间的变化。

---

## 2. 轨迹分析与绘图实践

以下将通过三个典型的分析案例——**SASA**, **RMSD**,  **Rg** 和 **RMSF**——来展示完整的工作流程。

### 2.1. 溶剂可及表面积 (SASA) 分析

溶剂可及表面积（Solvent Accessible Surface Area, SASA）用于衡量蛋白质或复合物暴露在溶剂中的表面积大小，其变化可以反映构象的紧凑程度。

#### 步骤 1: 准备 `cpptraj` 输入脚本 (`sasa.in`)

创建一个脚本文件，指令 `cpptraj` 加载文件并执行 SASA 计算。

```cpp
# sasa.in
# 1. 加载拓扑文件
parm complex_ions.prmtop
# 2. 加载轨迹文件
trajin complex_ions_md.nc
# 3. 执行 SASA 分析 (使用 LCPO 算法) 并输出到 sasa.dat
surf out sasa.dat
# 4. 运行
run
```

#### 步骤 2: 运行 `cpptraj`

在终端中执行以下命令：
```bash
~/software/amber20/bin/cpptraj sasa.in
```
执行后会生成 `sasa.dat` 文件，其内容格式为：
```
#Frame  SA_00001
1       14782.6102
2       14692.1938
...
```

#### 步骤 3: 使用 Python 处理数据并绘图

`cpptraj` 的输出是以**帧 (Frame)** 为单位的。为了获得更直观的时间序列图，我们需要将其转换为以**时间 (ns)** 为单位。

转换公式为：
`Time (ns) = Frame * ntwx * dt * 0.001`
（其中 `ntwx` 和 `dt` 在 `md.in` 文件中定义，通常 `ntwx * dt` 为 10 ps 或 0.01 ns）

以下是完整的 Python 绘图脚本：

```python
import matplotlib.pyplot as plt
import numpy as np

# --- 数据读取与转换 ---
# 适合单个文件处理的通用脚本
time_ns = []
sasa_values = []

with open('sasa.dat', 'r') as f_in, open('sasa_ns.dat', 'w') as f_out:
    for line in f_in:
        if line.startswith('#'):
            continue
        cols = line.split()
        frame = float(cols)
        sasa = float(cols)
        
        # 将 Frame 转换为 Time (ns)
        time = frame * 0.01 
        
        time_ns.append(time)
        sasa_values.append(sasa)
        f_out.write(f"{time:.6f}\t{sasa}\n")

# --- 使用 Matplotlib 绘图 ---
plt.figure(figsize=(10, 6))
plt.plot(time_ns, sasa_values, linestyle='-', color='blue', label='System SASA')
plt.xlabel('Time (ns)', fontsize=14)
plt.ylabel('SASA (Å²)', fontsize=14)
plt.title('SASA over Time', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.savefig('sasa_plot.png')
# plt.show()
```

### 2.2. 均方根偏差 (RMSD) 分析

均方根偏差（Root Mean Square Deviation, RMSD）用于衡量模拟过程中结构相对于一个参考结构（通常是初始结构或平衡结构）的偏离程度，是判断模拟体系是否达到平衡的重要指标。

#### 步骤 1: 准备 `cpptraj` 输入脚本 (`rmsd.in`)

```cpp
# rmsd.in
# 加载拓扑和轨迹
parm complex_ions.prmtop
trajin complex_ions_md.nc
# 使用平衡后的结构作为参考
reference complex_ions_eq.rst
# 计算残基 1-303 的 Cα 原子的 RMSD，忽略氢原子
rms ToFirst :1-303&!@H= first out rmsd.dat
run
```

#### 步骤 2: 运行 `cpptraj` 并绘图

执行 `cpptraj rmsd.in`。后续的数据处理和绘图流程与 SASA 分析完全相同，只需将文件名和坐标轴标签相应修改即可。最终可以得到 RMSD 随时间变化的曲线图。

### 2.3. 回旋半径 (Rg) 分析

回旋半径（Radius of Gyration, Rg）用于衡量体系结构的紧凑程度。Rg 值越小，表明结构越紧密。

#### 步骤 1: 准备 `cpptraj` 输入脚本 (`RoG.in`)

```cpp
# RoG.in
parm complex_ions.prmtop
trajin complex_ions_md.nc
# 计算残基 1-303 中非氢原子的质量加权回旋半径
radgyr :1-303&!(@H=) out RoG.dat mass nomax
run
```

#### 步骤 2: 运行 `cpptraj` 并绘图

同样，执行 `cpptraj RoG.in` 后，使用与 SASA 类似的 Python 脚本进行数据处理和绘图。

### 2.4. 均方根涨落 (RMSF) 分析

均方根涨落（Root Mean Square Fluctuation, RMSF）用于衡量模拟过程中每个残基（或原子）相对于其平均位置的涨落幅度，可以反映蛋白质各个区域的柔性。

#### 步骤 1: 准备 `cpptraj` 输入脚本 (`rmsf.in`)

```cpp
# rmsf.in
parm complex_ions.prmtop
trajin complex_ions_md.nc
# 计算所有残基 Cα 原子的 RMSF
rmsf RMSF_ref :1-303@CA out rmsf.dat
go
```

#### 步骤 2: 运行 `cpptraj` 并绘图

执行 `cpptraj rmsf.in` 后，使用 Python 绘图。注意，RMSF 的横坐标是**残基索引 (Residue Index)**，而不是时间。

```python
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = np.loadtxt('rmsf.dat', skiprows=1)
residue_index = data[:, 0] # 或者使用 range(1, len(data)+1) 创建
rmsf_values = data[:, 1]

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(residue_index, rmsf_values, linestyle='-', color='green')
plt.xlabel('Reside Index', fontsize=14)
plt.ylabel('RMSF (Å)', fontsize=14)
plt.title('RMSF per Residue', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('rmsf_plot.png')
# plt.show()
```

---

## 3. 多结果合并绘图

为了方便比较不同体系或不同模拟条件下的结果，我们可以将多份数据文件绘制在同一张图表中。

以下 Python 脚本演示了如何读取两个处理好的数据文件（例如 `sasa_ns_1.dat` 和 `sasa_ns_2.dat`），并将它们的数据绘制在一起。

```python
import matplotlib.pyplot as plt
import numpy as np

# --- 读取数据 ---
data1 = np.loadtxt('path/to/results1.dat')
time1 = data1[:, 0]
values1 = data1[:, 1]

data2 = np.loadtxt('path/to/results2.dat')
time2 = data2[:, 0]
values2 = data2[:, 1]

# --- 创建图形 ---
plt.figure(figsize=(12, 7))

# --- 绘制数据 ---
plt.plot(time1, values1, label='System 1: 6w81:Mpro', linestyle='-', color='blue')
plt.plot(time2, values2, label='System 2: 7mc9:PLpro', linestyle='-', color='red')

# --- 添加标题和标签 ---
plt.xlabel('Time (ns)', fontsize=14)
plt.ylabel('SASA (Å²)', fontsize=14) # 根据实际分析内容修改
plt.title('Comparison of SASA over Time', fontsize=16) # 根据实际分析内容修改

# --- 添加图例和网格 ---
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# --- 保存图像 ---
plt.savefig('comparison_plot.png')
print("Comparison plot saved as comparison_plot.png")
# plt.show()
```
通过修改标签和读取的文件，此脚本可通用地用于比较 SASA, RMSD, Rg 等多种分析结果。

