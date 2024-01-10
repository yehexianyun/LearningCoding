**# stata框架集
// 设置参数
global github "https://raw.githubusercontent.com/zhangdashenqi"
webuse set "${github}/the_zen_of_stata/master/data"

// 载入股票数据
webuse stock.dta, clear
frame create 账面价值 //创建一个名为账面价值的数据框；
frame 账面价值: webuse bookValue.dta, clear //指定在账面价值数据框中执行webuse bookValue.dta, clear命令，用于载入bookValues.dta数据集。
frame dir   // 查询内存中的所有数据框
frame rename default 股票数据 //将default命名为股票数据
frame pwf      // 查询当前工作的数据框

**#STATA实证命令
**# 1.1 更好的命令
shellout "file_name" //打开各类文件
codebook //数据概览
fsum, s(mean sd p50 min max) cat(rep78 foreign) label //更好的描述性统计
logout,save ("$Out\Table1 sum")word replace: tabstat price wei len mpg turn foreign, stat(mean sd p50 min max) format(%7.2f) column(statistic) //导出统计结果到word
**# 数据处理小技巧
tab year,gen(year)//生成年份虚拟变量
//如何将日期格式数据提取为年月日三个数据
gen new_year = year(date) //提取为年份
gen new_month = month(date) //提取为月份
gen new_date = day(date) //提取为日期
//如何将年份与月份合并为年月
gen year_month = ym(new_year,new_month) //合并年月变量
format year_month %tm //修改数据格式为年月
**# 如何将文本格式的日期转换为日期格式
generate date1 = date(date, "YMD")
gen date2 = date1
format date2 %td
//如何对文本进行筛选
keep if strmatch(variable, "*string*")
//字符转换成数值格式
destring variable, replace force
destring variable, gen(new_variable) ignore("*") //在转换为数值型变量时，忽略*符号
//Stata简单统计量
ameans x //计算变量x的算术平均值、几何平均值和简单调和平均值，均显示样本量和置信区间
mean var1 [pweight = var2] //求取分组数据的平均值和标准误，var1为各组的赋值，var2为每组的频数
tabstat X1,stats(mean n q max min sd var cv) //（计算变量X1的算术平均值、样本量、四分位线、最大最小值、标准差、方差和变异系数）
sort variable [,stable] //stable表示当有重复值时保持原顺序
gsort -x, generate(id) mfirst//对数据按x进行降序排列，缺失值排最前，生成反映位次的变量id
pwcorr 变量，sig star(0.05) //计算相关系数及显著性
**# 数据导入
use make price using "D:\Program Files\Stata17\auto.dta" //仅导入数据集中的部分变量
use "D:\Program Files\Stata17\auto.dta" in 1\10 //打开数据集的第1到第10个样本
use "D:\Program Files\Stata17\auto.dta" if foreign==1 //打开符合条件的数据
**# 数据处理
replace lnx1 =0 if missing(lnx1) //填充缺失值为 0
**# 尾部处理
winsor2 varlist [if] [in], [suffix(string) replace trim cuts(# #) by(groupvar) label]
**# 结果导出命令
est store m
reg2docx m using "outcome.docx", replace