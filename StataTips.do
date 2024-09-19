**# 基本编辑
edit var1 var2//仅编辑var1 var2变量
//contract命令将Stata数据集简化为多个变量；以及它们的频率。
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
**# 循环格式
global varlist "var1 var2 var3" //定义全局变量，要循环的内容
foreach var of $varlist {
    reg `var' x1 x2 x3 //循环内容
    est store `var'
}
forvalues i = 1/10 {  
    reg y x1 x2 x3 if id == `i' //循环内容
    est store m`i'
}
**# 文件循环

**# 字符序列与数值序列同时循环
global y 安徽	北京	福建	甘肃	广东	广西	贵州	海南	河北	河南	黑龙江	湖北	湖南	吉林	江苏	江西	辽宁	内蒙古	宁夏	青海	山东	山西	陕西	上海	四川	天津	新疆	云南	浙江	重庆
replace a = 1 //以变量为计数器
replace code =.
foreach i in $y{
	local b = a[1]  //循环体内设定计数器
	replace code = `b' if id == "`i'"  //注意此处需要手动添加双引号变为字符串
	replace a = a + 1 //循环体内更新计数器
}

**# 关于egen
* 20220412---stata基础：产生新变量gen与egen
input id year x
1 2018 1
1 2019 1
1 2020 1
2 2018 2
2 2019 2
2 2020 2
3 2018 3
3 2019 3
3 2020 3
end

egen num = count(x) //计数
egen xgroup = group(id year) //组合
gen xgroup2 =_n //与上一行命令等价，_n 是内部序号，不可见
gen num2 = count(x) //报错，因为应该用egen
egen xmax = max(x)
egen xmin = min(x)
egen xmean = mean(x)
egen xmedian = median(x)
egen xsd = sd(x) 
//求标准差[(1-2)^2*3+0+(3-2)^2*3]/(9-1)，再开根号
gen xsd2 = (6/8)^(0.5) 
egen x50 = pctile(x),p(50) //求二分位数
egen x25 = pctile(x),p(25) //求四分位数
//求分位数，该分位数对应概率为p
egen xtotal =total(x)
gen hong = xmax + xmin //相当于2个矩阵相加
gen hong2 = x + xmin
gen hong3 = "wisteria" //新建一个变量，且这个变量所有的观测值都为字符串
/*
如果表里已有观测值，直接 gen var1 = "wisteria"
啥都没有，要先确定观测值数量，比如 set obs 10；然后再gen var1 = "Italy"
*/

**# Stata绘图
**#1. 字体设定
local zh1 `"fontface "宋体":"'     // 中文字体 1
local zh2 `"fontface "黑体":"'     // 中文字体 2
local en1 `"fontface "times": "'   // 英文和数字字体 
local en2 `"fontface "courier new": "'   // 英文和数字字体 

sysuse "auto.dta", clear
twoway scatter price wei , ///
       ytitle(`"{`zh1' 汽车价格}{ `en1' (Price)}"') ///  
       xtitle(`"{`zh2' 重量 (磅)}{`en2' (Weight)}"')
graph export "Stata_Fig_diff_FontFace_02.png", width(700) replace 

**# Stata日期处理
//对于日期变量date
gen ym=mofd(date) //如果变成月度数据
gen ym=yofd(date) //如果变成年度数据
gen yq=qofd(date) //如果变成季度数据


gen week = dow(date) //使用日期数据计算星期几
collapse (mean) gpa hour, by(year) //分组求和   

**# 导出各种表格
sum2docx [varlist] using d:/mytable.docx, replace stats(N mean(%6.2f) sd min(%6.0g) median(%6.0g) max(%6.0g)) title("The Summary Statistics") 

**# 新命令
labone,nrow(1)//采用 labone 命令可以方便快捷地设定变量标签名为指定行的观测值内容。
//采用 nrow 命令可以将指定行的变量观测值命名为变量名
net install sgmediation2, from("https://tdmize.github.io/data/sgmediation2")//安装新的中介效应检验sgmediation2
