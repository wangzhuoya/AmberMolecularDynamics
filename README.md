# Amber Molecular Dynamics
通过Amber来运行分子动力学模拟。

## 1. 安装Amber/AmberTools/Acpype

## 2. “小分子-蛋白”复合体模拟

### 2.1. 处理蛋白结构
蛋白的预处理比较简单，只需要将从RCSB PDB数据库中获取的蛋白部分进行质子化即可，在剔除非蛋白部分的原子后，使用AmberTools中的pdb4amber完成蛋白质的加氢。
```bash
conda activate AmberTools21
pdb4amber -i test.pdb -o rec.pdb -y --reduce
```
- 输入：4TPW-pro.pdb
- 输出：**rec.pdb**

### 2.2 处理小分子
对接后的小分子生成amber参数文件
```bash
# conda activate AmberTools21
acpype -i test.mol2 -a gaff2 -c bcc -n 0
```
-i：输入文件，建议为mol2格式，其他格式将通过openbabel转换；

-a：小分子力场参数；

-c：电荷类型；

-n：电荷数；

之所以选择gaff2力场，是因为该力场涵盖了大多数的元素。bcc电荷是一种半经验的拟合静电势电荷，计算速度极快，操作简单，包含在Antechamber中，虽然比起RESP电荷而言精度较低，但无需依赖额外的程序。


### 2.3. 生成amber格式的拓扑文件
利用Leap/Tleap程序完成“小分子-蛋白”复合物amber参数体系的构建。
```bash
# conda activate AmberTools21
tleap -f  tleap.leaprc
```
- 输入：tleap.leaprc
- 输出：complex_ions.inpcrd 和 complex_ions.prmtop


### 2.4. 模拟
```bash
nohup bash amber_run.sh >md.log 2>&1 &
```
- 输入：amber_run.sh、complex_ions.inpcrd 、complex_ions.prmtop、eq.in、heat.in、md.in、min1.in、min2.in、mmpbsa.in、press.in


## 3. 蛋白模拟
### 3.1. 处理蛋白结构
蛋白的预处理比较简单，只需要将从RCSB PDB数据库中获取的蛋白部分进行质子化即可，在剔除非蛋白部分的原子后，可以使用AmberTools中的pdb4amber完成蛋白质的加氢。具体的加氢程序是由杜克大学的Richardson实验室开发的Reduce程序完成。
```bash
conda activate AmberTools21
pdb4amber -i test.pdb -o rec.pdb -y --reduce
```
- 输入：4TPW-pro.pdb
- 输出：rec.pdb

### 3.2. 生成amber格式的拓扑文件
利用Leap/Tleap程序完成“小分子-蛋白”复合物amber参数体系的构建。
```bash
# conda activate AmberTools21
tleap -f  tleap.leaprc
```
- 输入：tleap.leaprc
- 输出：rec_ions.inpcrd 和 rec_ions.prmtop


### 3.3. 模拟
```bash
nohup bash amber_run.sh >md.log 2>&1 &
```
- 输入：amber_run.sh、rec_ions.inpcrd 、rec_ions.prmtop、eq.in、heat.in、md.in、min1.in、min2.in、mmpbsa.in、press.in





## 4. 分析作图
当分子动力学模拟结束后就可以用amber中自带的cpptraj程序进行轨迹分析。

