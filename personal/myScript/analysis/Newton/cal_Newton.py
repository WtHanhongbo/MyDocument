#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import  xlrd
import sys
import random
import numpy as np
from sympy import *


#已知数据的数量
ICOUNT = 15 


#需要计算的期数序数
NextTerm = 24014 

#已知数据的来源表格
EXCELFILE = "../previous_data.xls"

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

def Get_Excel_colNum(filePath,SheetNo):

    workbook = xlrd.open_workbook(filePath)
    sheet = workbook.sheets()[SheetNo]   #通过索引顺序获取
    #sheet = workbook.sheet_by_name("Sheet1")  #通过名称获取   
    number = sheet.nrows 

    return number


if __name__=="__main__":

    # 获取参数
    paras = sys.argv[1:]
    print("the length of paras is: %s"%(len(paras)))
    # 如果执行脚本时带有参数，从脚本参数获取iCount的值
    if (len(paras) > 0):
        print("paras[0] == %s"%(paras[0]))
        ICOUNT = int(paras[0])
    # 保存最终输出的结果, 固定为 “6+1=7” 个
    iResult_1 = [0] * 7
    iResult_2 = [0] * 7
    iResult_3 = [0] * 7
     
    # 保存自变量，第0列，期数
    x_value = np.arange(1,ICOUNT+1,1)
    N_ColNum = Get_Excel_colNum(EXCELFILE,0)    

    print("The cal base number is： %s"%ICOUNT) 
    print("the mount of excel lines is：%s"%N_ColNum) 
    if (ICOUNT >= N_ColNum):
        print ("ICOUNT >= N_ColNum, error, exit" )
        exit()
    
    for i in range(ICOUNT): 
        x_value[i] = Read_Excel(EXCELFILE,0,N_ColNum-ICOUNT+i,0) 
    
    print("the first col x_value is： %s"%x_value)  



    
    # 从表格读取
    VolData = [0]* ICOUNT

    # j 从0 循环到 7
    for j in range(7): 
        print("The %s ’th data begin:"%(j+1))

        # 读取表格的第 j+1 列
        for i in range(ICOUNT): 
            VolData[i] = Read_Excel(EXCELFILE,0,N_ColNum-ICOUNT+i,j+1)

        y_value = VolData
        print("line 92: y_value is %s"%y_value)
    
        newton_function = Newton(x_value,y_value)
        print("N(x)=",newton_function)
    
        iResult_1[j] = newton_function.evalf(subs={X:NextTerm})

    
    print("The data_1 which newton interpolation is: %s"%iResult_1)
        
    for i in range(7):
        iResult_2[i] = round(iResult_1[i])
        
    print("The data_2 which int form data_1 is: %s"%iResult_2)        

    for i in range(6):
        iResult_3[i] = iResult_2[i] % 33

    iResult_3[6] = iResult_2[6] % 16
    
    print("The data_3 which modify data_2 to correct range is: %s"%iResult_3)
