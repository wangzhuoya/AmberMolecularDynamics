# AMBER 分子动力学模拟工作流

本文档旨在提供一个清晰、可复现的分子动力学（MD）模拟工作流，主要使用 AMBER、AmberTools 、acpype 和 cpptarj 套件。整个流程分为三个主要部分：**小分子参数化**、**蛋白质-小分子复合物模拟**以及**轨迹分析**。

---


## 1. 小分子力场参数化

在进行复合物模拟之前，首先需要为小分子（配体）生成符合 AMBER 力场标准的参数文件。我们推荐使用 `acpype` 工具来自动化这一过程。

### 1.1. 生成小分子拓扑文件

使用 `acpype` 可以方便地从小分子结构文件（如 `.mol2`）生成 AMBER 所需的拓扑和坐标文件。

```bash
# 激活 AmberTools 环境包含（Acpype）
conda activate AmberTools21

# 运行 acpype
acpype -i test.mol2 -a gaff2 -c bcc -n 0
```

**命令参数解析:**
*   `-i test.mol2`: 指定输入的分子结构文件。推荐使用 `.mol2` 格式，其他格式 `acpype` 会尝试通过 OpenBabel 自动转换。
*   `-a gaff2`: 指定使用 **GAFF2** (General AMBER Force Field 2) 力场。我们选择此力场是因为其参数覆盖了绝大多数有机小分子，适用性广。
*   `-c bcc`: 指定使用 **AM1-BCC** 方法计算原子部分电荷。这是一种半经验方法，计算速度极快且无需依赖外部量子化学程序，是速度与精度之间的一个优秀平衡点。
*   `-n 0`: 指定分子的总电荷。请根据您的分子实际情况修改（例如，-1, 1）。

**执行完毕后，您将获得 `test.prmtop` 和 `test.inpcrd` 等文件，这些是后续步骤的必要输入。**

---

## 2. 蛋白质-小分子复合物模拟

本部分将详细介绍如何构建蛋白质-小分子复合物体系，并运行分子动力学模拟。

### 2.1. 蛋白质结构预处理

从 [RCSB PDB](https://www.rcsb.org/) 数据库下载的蛋白质结构通常需要进行预处理，包括添加缺失的氢原子、处理非标准残基等。我们使用 AmberTools 内置的 `pdb4amber` 工具来完成这一任务。

```bash
# 激活 AmberTools 环境
conda activate AmberTools21

# 预处理 PDB 文件
pdb4amber -i test.pdb -o rec.pdb -y --reduce
```

**命令解析:**
*   `-i test.pdb`: 输入原始的 PDB 文件。
*   `-o rec.pdb`: 输出处理完毕、符合 AMBER 规范的 PDB 文件。
*   `--reduce`: 调用 Reduce 程序来添加和优化氢原子网络，确保蛋白质的质子化状态合理。
*   `-y`: 覆盖已存在的输出文件。

### 2.2. 构建复合物体系拓扑

接下来，我们使用 AMBER 的 `tleap` 模块将处理好的蛋白质 (`rec.pdb`) 和第一步中参数化的小分子结合起来，并添加溶剂和离子，最终生成整个模拟体系的拓扑 (`.prmtop`) 和坐标 (`.inpcrd`) 文件。

```bash
# 激活 AmberTools 环境
# conda activate AmberTools21  # 如果已在环境中则无需重复执行

# 运行 tleap
tleap -f tleap.leaprc
```

**工作流:**
*   **输入**:
    *   `tleap.leaprc`: 这是一个 `tleap` 的**脚本文件**，您需要提前编写好。它定义了加载力场、加载分子结构、添加溶剂盒子、添加平衡离子等一系列指令。
*   **输出**:
    *   `complex_ions.prmtop`: 描述整个复合物体系（蛋白质+配体+水+离子）的力场和连接信息。
    *   `complex_ions.inpcrd`: 包含整个体系初始原子坐标。

### 2.3. 运行分子动力学模拟

所有准备工作完成后，即可开始运行 MD 模拟。我们提供了一个标准化的执行脚本 `amber_run.sh`，其中包含了能量最小化、加热、平衡和生产模拟等一系列步骤。

为了让模拟在后台稳定运行，我们使用 `nohup` 命令：

```bash
nohup bash amber_run.sh > md.log 2>&1 &
```

**命令解析:**
*   `nohup ... &`: 确保即使您关闭了终端，模拟任务也能在服务器后台继续运行。
*   `> md.log 2>&1`: 将所有的标准输出和错误输出都重定向到 `md.log` 文件中，方便后续检查模拟的运行状态和可能的错误。

**运行此模拟需要以下输入文件：**
*   **执行脚本**: `amber_run.sh`
*   **体系文件**: `complex_ions.prmtop`, `complex_ions.inpcrd`
*   **AMBER 输入参数**: `min1.in`, `min2.in`, `heat.in`, `press.in`, `eq.in`, `md.in` 等。

---

## 3. 轨迹分析与可视化

当长时间的生产模拟结束后，您将获得一个或多个轨迹文件（通常是 `.nc` 格式）。此时，可以使用 AMBER 内置的强大分析工具 `cpptraj` 来进行后续处理和数据分析。

**常见分析内容包括：**
*   计算均方根偏差 (RMSD)
*   计算均方根涨落 (RMSF)
*   计算溶剂可及表面积 (SASA)
*   计算回转半径 (Rg)

使用 `cpptraj` 进行分析通常也需要编写一个输入脚本，然后执行它来处理轨迹数据。

```bash
# 示例：运行 cpptraj 分析
cpptraj -p complex_ions.prmtop -i cpptraj.in
```


---
