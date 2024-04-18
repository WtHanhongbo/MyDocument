#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import  xlrd
import numpy as np
from sympy import *

#已知数据的数量
ICOUNT = 5

#已知数据的来源表格
EXCELFILE = "data.xls"

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

##########################################################################
#    拉格朗日插值函数
#    参数：
#        x_points: 已知数据点的x坐标列表或numpy数组
#        y_points: 对应于x_points的y坐标列表或numpy数组
#        x_target: 需要进行插值的目标x值
#    返回：
#        y_interpolated: 插值计算出的目标x值对应的y值
##########################################################################
def lagrange_interpolation(x_points, y_points, x_target):
    
    length = len(x_points)
    lagrange_polynomial = 0
    
    for i in range(length):
    
        li = y_points[i]
        
        for j in range(length):
            if i != j:
                li *= (x_target - x_points[j]) / (x_points[i] - x_points[j])

        lagrange_polynomial += li
    return lagrange_polynomial

# 示例数据
# x_data = np.array([1.0, 2.0, 3.0, 4.0])
# y_data = np.array([5.0, 9.0, 17.0, 33.0])

# 目标x值
# x_to_interpolate = 2.5

# 使用拉格朗日插值计算目标值
# y_interpolated = lagrange_interpolation(x_data, y_data, x_to_interpolate)
# print(f"在x={x_to_interpolate}处的插值结果为：y={y_interpolated}")

if __name__=="__main__":

    # 保存最终输出的结果, 固定为 “6+1=7” 个
    iResult_1 = [0] * 7
    iResult_2 = [0] * 7
    iResult_3 = [0] * 7

    N_ColNum = Get_Excel_colNum(EXCELFILE,0)
    print("line 76: ICOUNT is %s"%ICOUNT) 
    print("line 77: N_ColNum is %s"%N_ColNum) 
    
    # 保存自变量，第0列，期数
    x_value = np.arange(1,ICOUNT+1,1)
    for i in range(ICOUNT): 
        x_value[i] = Read_Excel(EXCELFILE,0,N_ColNum-ICOUNT+i,0) 
    x_to_interpolate = x_value[ICOUNT-1] + 1   

    print("line 74: x_value is %s"%x_value)  
    print("line 75: x_to_interpolate is %s"%x_to_interpolate)
    
    # 从表格读取
    VolData = [0]* ICOUNT


    # j 从0 循环到 7
    for j in range(7): 
        print("line 81：The %s ’th data begin:"%(j+1))

        # 读取表格的第 j+1 列
        for i in range(ICOUNT): 
            VolData[i] = Read_Excel(EXCELFILE,0,N_ColNum-ICOUNT+i,j+1)

        #####暂时先保持现状：后面考虑表格转为CSV，从文档末尾取倒数 ICOUNT 行。 可能会有转置操作
        y_value = VolData
        print("line 102: y_value is %s"%y_value)
    
        y_interpolated = lagrange_interpolation(x_value, y_value, x_to_interpolate)
        
        print("line 106： y_interpolated=",y_interpolated)
    
        iResult_1[j] = y_interpolated

    
    print("line 111： The first data iResult_1 === %s"%iResult_1)
        
    for i in range(7):
        iResult_2[i] = round(iResult_1[i])
        
    print("line 116： The second data iResult_2 === %s"%iResult_2)        

    for i in range(6):
        iResult_3[i] = iResult_2[i] % 33

    iResult_3[6] = iResult_2[6] % 16
    
    print("line 123：The third data iResult_3 === %s"%iResult_3)
