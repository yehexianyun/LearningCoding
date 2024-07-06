*--------------------------
* xianyunyehe 的 dofile 文档
*--------------------------


*-说明：
* 此文件设定了每次启动 stata 时需要做的一些基本设定
* 更多相关设定： help set

**# 不要自动更新
set update_query  off  // on

**# 参数设定
global path "G:/WorkDirectory/Stata" //统一存放地址
sysdir set PLUS `"$path/plus"'
sysdir set PERSONAL `"$path/personal"'
set type double           // 设定 generate 命令产生的新变量为双精度类型
set matsize 800           // 设定矩阵的维度为 800x800, 可以修改，上限为 11000
set scrollbufsize 2000000 // 结果窗口中显示的行数上限
set more off, perma       // 关闭分页提示符

**# 中文编码
unicode analyze * //任何文件类型皆可
unicode encoding set gb18030 //获取 Stata 的提示信息
unicode translate * //这行代码需要根据 Stata 的提示信息来撰写，并不一定与这里列出的代码一模一样


**# 自动记录日志文件

cap cd `"$path/do"'
if _rc{
	mkdir `"$path/do"'
}

local filename_time = subinstr("`c(current_time)'",":","-",2)
local filename_date = subinstr("`c(current_date)'"," ","",3)
log using $path/do/log-`filename_date'-`filename_time'.smcl, text replace
cmdlog using $path/do/cmd-`filename_date'-`filename_time'.log,replace

**# 自动切换工作目录

cd `"`c(sysdir_personal)'"' 
