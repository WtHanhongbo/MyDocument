#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import  xlrd
import sys
import random
import numpy as np
from sympy import *

#已知数据的数量, 默认为5；调用脚本时也可以以参数形式带入
ICOUNT = 5

#已知数据的来源表格
EXCELFILE = "../previous_data.xls"

def Read_Excel(filePath,SheetNo,RowNum,ColNum):

    workbook = xlrd.open_workbook(filePath)
    sheet = workbook.sheets()[SheetNo]   #通过索引顺序获取
    #sheet = workbook.sheet_by_name("Sheet1")  #通过名称获取   
    number = sheet.cell_value(RowNum,ColNum) #返回单元格中的数据

    return number

def Get_Excel_colNum(filePath,SheetNo):

    workbook = xlrd.open_workbook(filePath)
    sheet = workbook.sheets()[SheetNo]   #通过索引顺序获取
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
    iResult_4 = [0] * 7

    #获取表格数据总行数
    N_ColNum = Get_Excel_colNum(EXCELFILE,0)
    
    print("The cal base number is： %s"%ICOUNT) 
    print("the mount of excel lines is：%s"%N_ColNum) 
    
    if (ICOUNT >= N_ColNum):
        print ("ICOUNT >= N_ColNum, error, exit" )
        exit()
    
    # 保存自变量，第0列，期数， 初始化为全1
    x_value = np.arange(1,ICOUNT+1,1)

    # 读取表格第一列
    for i in range(ICOUNT): 
        x_value[i] = Read_Excel(EXCELFILE,0, N_ColNum - ICOUNT + i, 0) 

    # 预测的期数
    x_to_interpolate = x_value[ICOUNT-1] + 1   

    print("the first col x_value is： %s"%x_value)  
    print("x_to_interpolate is %s"%x_to_interpolate)
    
    # 从表格读取
    VolData = [0]* ICOUNT

    # iResult_1 差值结果
    # j 从0 循环到 7
    for j in range(7): 
        print("The %s ’th data begin:"%(j+1))

        # 读取表格的第 j+1 列
        for i in range(ICOUNT): 
            VolData[i] = Read_Excel(EXCELFILE,0, N_ColNum - ICOUNT + i,j+1)

        y_value = VolData
        print("y_value is %s"%y_value)
    
        y_interpolated = lagrange_interpolation(x_value, y_value, x_to_interpolate)
        
        print("y_interpolated=",y_interpolated)
    
        iResult_1[j] = y_interpolated

    
    print("The data_1 which lagrange interpolation is: %s"%iResult_1)

    # iResult_2： 对iResult_1 取整        
    for i in range(7):
        iResult_2[i] = round(iResult_1[i])
        
    print("The data_2 which int form data_1 is: %s"%iResult_2)        

    # iResult_3： 对iResult_2取余，修正到正确的区间 
    for i in range(6):
        iResult_3[i] = iResult_2[i] % 33

    iResult_3[6] = iResult_2[6] % 16
    
    print("The data_3 which modify data_2 to correct range is: %s"%iResult_3)
    
    # iResult_4： 对iResult_3 随机化
    for i in range(6):
        iResult_4[i] = round(iResult_3[i] * random.random()) % 33

    iResult_4[6] = round(iResult_3[6] * random.random()) % 33

    print("The data_4 which to make data_3 random is: %s"%iResult_4)    
    
    
