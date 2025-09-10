在运行Amber之前，需要预先安装Amber_AmberTools_Acpype

## 安装依赖

### 1. CentOS 7
请根据操作系统的类型选择[安装教程](https://ambermd.org/Installation.php)。
编译Amber需要预先安装以下依赖。
```bash
yum -y install tcsh make \
               gcc gcc-gfortran gcc-c++ \
               which flex bison patch bc \
               libXt-devel libXext-devel \
               perl perl-ExtUtils-MakeMaker util-linux wget \
               bzip2 bzip2-devel zlib-devel tar
```

### 2.安装AmberTools(via conda)

```bash
conda create --name AmberTools python=3.12 
conda activate AmberTools
conda install dacase::ambertools-dac=25
```
### 3. 安装Acpype
Acpype基于AmberTools/Antechamber，能够帮生成CNS/XPLOR、GROMACS、CHARMM和Amber等MD软件的拓扑参数文件。对于我们这种既使用GROMACS又使用Amber的人来说十分友好。
pip安装十分简单，比较推荐将Acpype也安装在AmberTools的环境中，一起使用比较方便。
```bash
pip install acpype
```

### 4. 安装Amber
Amber软件分为商业授权和非商业授权，非商业授权需要edu的邮箱区申请下载链接。
```bash
cd amber22_src/build
# optional: edit the run_cmake script to make any needed changes;
# most users should not need to do this
./run_cmake
# Next, build and install the code:
make install
```


### 5. 解决conda: command not found
服务器重启后找不到conda了，需要重启conda
```bash
conda init bash
```
执行后需要重启终端后即可进入conda的base环境。



## 参考文献
1. R. Salomon-Ferrer, D.A. Case, R.C. Walker. An overview of the Amber biomolecular simulation package. WIREs Comput. Mol. Sci. 3, 198-210 (2013). (PDF)
2. D.A. Case, T.E. Cheatham, III, T. Darden, H. Gohlke, R. Luo, K.M. Merz, Jr., A. Onufriev, C. Simmerling, B. Wang and R. Woods. The Amber biomolecular simulation programs. J. Computat. Chem. 26, 1668-1688 (2005).
3. D.A. Case, H.M. Aktulga, K. Belfon, D.S. Cerutti, G.A. Cisneros, V.W.D. Cruzeiro, N. Forouzesh, T.J. Giese, A.W. Götz, H. Gohlke, S. Izadi, K. Kasavajhala, M.C. Kaymak, E. King, T. Kurtzman, T.-S. Lee, P. Li, J. Liu, T. Luchko, R. Luo, M. Manathunga, M.R. Machado, H.M. Nguyen, K.A. O’Hearn, A.V. Onufriev, F. Pan, S. Pantano, R. Qi, A. Rahnamoun, A. Risheh, S. Schott-Verdugo, A. Shajan, J. Swails, J. Wang, H. Wei, X. Wu, Y. Wu, S. Zhang, S. Zhao, Q. Zhu, T.E. Cheatham III, D.R. Roe, A. Roitberg, C. Simmerling, D.M. York, M.C. Nagan*, and K.M. Merz Jr.* AmberTools. J. Chem. Inf. Model. 63, 6183-6191 (2023).
