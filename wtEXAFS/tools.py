# -*- coding:utf-8 -*-

import tkinter.messagebox

from numpy import loadtxt

from wtEXAFS import para


# --------- 读入txt数据并返回k首尾值和间隔 ---------
def colFirstLastInter(path_name: str):
    column_data = loadtxt(path_name, skiprows=0)[:, 0]
    data1 = column_data[0]
    data2 = column_data[1]
    interval = data2 - data1
    firstLastInter = [column_data[0], column_data[-1], interval]
    return firstLastInter


# --------- 检测输入的字符串是否为大于零的整数 ---------
def testInt(input_str: str, reason, name):
    return_variable = False  # 设置默认返回值为False
    list1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]  # 设置默认检测数列
    if input_str != "0":
        for i in list1:  # for循环来检测最新输入的字符是否满足要求
            if input_str == "" or input_str[-1] == i:  # 条件不可以调换顺序，否则当输入框内无内容时content[-1]索引无效报错
                return_variable = True
                break
    else:
        return_variable = False
    return return_variable  # 返回值


# --------- 检测输入的字符串是否为大于零的整数串 ---------
def testMulInt(input_str: str, reason, name):
    return_variable = False  # 设置默认返回值为False
    list1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "]  # 设置检测数列
    if input_str != " ":
        for i in list1:  # for循环来检测最新输入的字符是否满足要求
            if input_str == "" or input_str[-1] == i:  # 条件不可以调换顺序，否则当输入框内无内容时content[-1]索引无效报错
                return_variable = True
                break
    else:
        return_variable = False
    return return_variable  # 返回值


# --------- 检测输入的字符串是否为大于零的数 ---------
def testFloat(input_str: str, reason, name):
    return_variable = False  # 设置默认返回值为False
    list1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]  # 设置默认检测数列
    # 检测输入框中是否已有小数点，如果存在就更改数列list1
    L_content = list(input_str)
    if len(input_str) > 1:
        del L_content[-1]
    for j in L_content:
        if j == ".":
            list1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            break
    for i in list1:  # for循环来检测最新输入的字符是否满足要求
        if input_str == "" or input_str[-1] == i:  # 这两个条件不可以调换顺序，否则当输入框内无内容时content[-1]索引无效报错
            return_variable = True
            break
    return return_variable  # 返回值


# --------- 检测输入的k/R/sigma/eta/n是否合理 ---------
def testKRInput(kmin: float, kmax: float, deltak: float, rmin: float, rmax: float, deltar: float, sigma: float,
                eta: float, norder: float):
    flag = False
    # --------- 判断输入是否合理 ---------
    if kmax <= kmin or kmax > para.Parameters.kmax or kmin < para.Parameters.kmin:
        pass
    elif rmax <= rmin or rmin == 0 or rmax == 0:
        pass
    elif deltak > (para.Parameters.kmin + para.Parameters.kmax) / 2 or deltar > (rmin + rmax) / 2:
        pass
    elif eta == 0.0 or sigma == 0.0 or norder == 1.0:
        pass
    else:
        # --------- 刷新Parameter类（用户更改k时实际上改的是b） ---------
        para.Parameters.bmin = kmin
        para.Parameters.bmax = kmax
        para.Parameters.db = deltak
        para.Parameters.Rmin = rmin
        para.Parameters.Rmax = rmax
        para.Parameters.dR = deltar
        para.Parameters.sigma = sigma
        para.Parameters.eta = eta
        para.Parameters.n = norder
        flag = True
    return flag


# ----------- 错误汇总 -----------
def messagesOrError(error_type: str):
    if error_type == "configAccepted":
        tkinter.messagebox.showinfo(title="Tips!", message="The config was accepted successfully!")
    elif error_type == "calculationDone":
        tkinter.messagebox.showinfo(title="Tips!", message="Calculation completed!")
    elif error_type == "config import":
        tkinter.messagebox.showinfo(title="Tips!", message="Config imported!")
    elif error_type == "inputOut":
        tkinter.messagebox.showwarning(title="Error!",
                                       message="The input of kmin/kmax/dk/Rmin/Rmax/dR were out of range!")
    elif error_type == "selectionOut":
        tkinter.messagebox.showwarning(title="Error!", message="Column or row selection were out of range!")
    elif error_type == "data import failed":
        tkinter.messagebox.showwarning(title="Error!", message="Data import failed, please try again!")
    elif error_type == "about":
        tkinter.messagebox.showinfo(title="About!",
                                    message="Author: Zhihang Ye " + "\n" +
                                            "School: China University of Geosciences (Wuhan)" + "\n" +
                                            "E-mail: yezhihang@live.com" + "\n" +
                                            "Python version: 3.7.9 (Windows 64-bit)" + "\n" +
                                            "Github: https://github.com/Himmelspol/wtEXAFS.git")
