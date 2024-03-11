#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import  xlrd
import numpy as np
from sympy import *


#已知数据的数量
ICOUNT = 3 

#需要计算的期数序数
NextTerm = 24014 

#已知数据的来源表格
EXCELFILE = "data.xls"

#定义自变量x
X = symbols("x")

 
def cs(x, f, start, end, res):
    if((end-start)==1):
        res[end-1][end-start-1]=(f[end]-f[start])/(x[end]-x[start])
        return res[end-1][end-start-1]

    res[end-1][end-start-1]=(cs(x,f,start+1,end,res)-cs(x,f,start,end-1,res))/(x[end]-x[start])
    return res[end-1][end-start-1]

def Newton(x,f):
     res = np.ones([x.size - 1, x.size - 1])*np.inf
     cs(x, f, 0, x.size - 1, res)
     X=symbols("x")
     y=f[0]
     for i in range(x.size-1):
         temp=1
         for j in range(i+1):
             temp=temp*(X-x[j])
         temp=res[i,i]*temp
         y=y+temp
     return y


def Read_Excel(filePath,SheetNo,RowNum,ColNum):

    workbook = xlrd.open_workbook(filePath)
    sheet = workbook.sheets()[SheetNo]   #通过索引顺序获取
    #sheet = workbook.sheet_by_name("Sheet1")  #通过名称获取   
    number = sheet.cell_value(RowNum,ColNum) #返回单元格中的数据

    return number


if __name__=="__main__":

    # 保存最终输出的结果, 固定为 “6+1=7” 个
    iResult_1 = [0] * 7
    iResult_2 = [0] * 7
    iResult_3 = [0] * 7
     
    # 保存自变量，第0列，期数
    x_value = np.arange(1,ICOUNT+1,1)
    for i in range(ICOUNT): 
        x_value[i] = Read_Excel(EXCELFILE,0,i+1,0) 
    
    print("line 61: x_value is %s"%x_value)    
    
    # 从表格读取
    VolData = [0]* ICOUNT

    # j 从0 循环到 7
    for j in range(7): 
        print("The %s ’th data begin:"%(j+1))

        # 读取表格的第 j+1 列
        for i in range(ICOUNT): 
            VolData[i] = Read_Excel(EXCELFILE,0,i+1,j+1)

        y_value = VolData
        print("line 80: y_value is %s"%y_value)
    
        newton_function = Newton(x_value,y_value)
        print("N(x)=",newton_function)
    
        iResult_1[j] = newton_function.evalf(subs={X:NextTerm})

    
    print("The first data iResult_1 === %s"%iResult_1)
        
    for i in range(7):
        iResult_2[i] = round(iResult_1[i])
        
    print("The second data iResult_2 === %s"%iResult_2)        

    for i in range(6):
        iResult_3[i] = iResult_2[i] % 33

    iResult_3[6] = iResult_2[6] % 16
    
    print("The third data iResult_3 === %s"%iResult_3)
