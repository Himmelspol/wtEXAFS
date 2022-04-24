# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import tkinter.messagebox
import tkinter.simpledialog
from numpy import array
from numpy import loadtxt

from wtEXAFS import path, para
from wtEXAFS.fileOper import valueList


# --------- 数据载入数据显示框（含行号，从1开始） ---------
def showTextInBox(self, data_content):
    self.show_scrolledBox.delete(1.0, "end")  # 先清空内容
    count = 1
    for line in data_content:  # 列表输出
        self.show_scrolledBox.insert("end", str(count) + "\t" + str(line))
        count += 1


# --------- k Weight数据绘图 ---------
def showKWeighted():
    kW_data = loadtxt(path.TempPath.get('kW'), skiprows=0)
    legend_note = loadtxt(path.TempPath.get('col_selection'), dtype=str)
    legend = legend_note.tolist()
    plt.close(1)
    fig_kw = plt.figure(1)
    fig_kw.canvas.set_window_title('Plot of k-weight chi(k)')
    plt.grid()
    plt.xlim((kW_data[:, 0][0], kW_data[:, 0][-1]))
    plt.xlabel("k (Å$^{-1}$)")
    plt.ylabel("k-weighted chi (k)")
    k = kW_data[:, 0]
    col_limits = kW_data.shape[1]
    for i in range(1, col_limits):
        temp_chik = kW_data[:, i]
        plt.plot(k, temp_chik, linewidth=1.2, label=legend[i - 1])
    plt.legend(loc='upper right', title="Column")
    print("Optional: Show your k-weighted chi data.")
    plt.show()


# --------- k和R数据绘图 ---------
def showKR():
    # 读取需要作图的数据
    kW_data = loadtxt(path.TempPath.get('kW_for_WT'), skiprows=0)
    window_data = loadtxt(path.TempPath.get("window"), skiprows=0)
    chiR_data = loadtxt(path.TempPath.get("R"), skiprows=0)
    legend_note = loadtxt(path.TempPath.get('col_selection'), dtype=str)
    legend = legend_note.tolist()
    # 进入画图细节
    plt.close(2)
    fig_kw = plt.figure(2, figsize=(10, 4))
    plt.subplots_adjust(left=0.1, bottom=0.12, right=0.96, top=0.90, wspace=0.18, hspace=None)
    fig_kw.canvas.set_window_title('Plot of chi(k) and chi(R)')
    # 第一个子图为k空间数据
    plt.subplot(121)
    plt.grid()
    plt.xlim((para.Parameters.kmin, para.Parameters.kmax))
    plt.xlabel("k (Å$^{-1}$)")
    plt.ylabel("k-weighted chi (k)")
    k = kW_data[:, 0]
    kcol_limits = kW_data.shape[1]
    for i in range(1, kcol_limits):
        temp_chik = kW_data[:, i]
        plt.plot(k, temp_chik, linewidth=1.2, label=legend[i - 1])
    plt.plot(window_data[:, 0], window_data[:, 1], label="window")  # 把窗函数画出来
    plt.legend(loc='upper right', title="Column", fontsize=8)
    print("Optional: Show your k-weighted chi data.")

    # 第二个子图为R空间数据
    plt.subplot(122)
    plt.grid()
    plt.xlim((0, 6))
    plt.xlabel("R (Å)")
    plt.ylabel("mag|FT[chi(k)]|")
    R = chiR_data[:, 0]
    rcol_limits = chiR_data.shape[1]
    for i in range(1, rcol_limits):
        temp_chiR = chiR_data[:, i]
        plt.plot(R, temp_chiR, linewidth=1.2, label=legend[i - 1])
    plt.legend(loc='upper right', title="Column", fontsize=8)
    print("Optional: Show your k-weighted chiR data.")
    plt.show()


# --------- 小波基的展示 ---------
def showMotherWavelet():
    MW_data = loadtxt(path.TempPath.get('mother_wavelet'), skiprows=0, dtype=complex)
    data_r = valueList("R").round(3)
    data_rmin = data_r[0]
    data_rmax = data_r[-1]
    data_index = len(MW_data[0]) - 1
    plt.close(3)
    fig_MW = plt.figure(3)
    fig_MW.canvas.set_window_title('Plot of mother wavelet')
    if tkinter.messagebox.showinfo(title="Tips",
                                   message="The user can enter different R to show different scaled wavelet"):
        input_r = tkinter.simpledialog.askfloat("Choose the R you want to show!",
                                                "Please select an R from " + str(data_rmin) + " to " + str(data_rmax))
        input_index = int((input_r - data_rmin) / para.Parameters.dR)
        if input_index in np.arange(data_index):
            k_show = array(MW_data[:, 0]).real
            MW = array(MW_data[:, input_index + 1]).real
            plt.title("R selection: " + str(data_r[input_index]))
            plt.grid()
            plt.xlim(para.Parameters.bmin, para.Parameters.bmax)
            plt.plot(k_show, MW)
            plt.legend(['real part'], loc='upper left')
            print("Optional: Show the wavelet according to the parameters.")
            plt.show()
        else:
            tkinter.messagebox.showinfo(title="Error",
                                        message="Out of range! Please enter again!")


# --------- 小波结果的展示 ---------
def showWaveletResult():
    # --------- 读入文件 ---------
    mesh_note = loadtxt(path.TempPath.get('mesh_note'), skiprows=0)
    wt_data = loadtxt(path.TempPath.get('WT'), skiprows=0)
    col_selection = loadtxt(path.TempPath.get('col_selection'), dtype=int, skiprows=0).tolist()
    # --------- 获得多列数据模式时的列限制 ---------
    cols = wt_data.shape[1]
    # --------- 获得小波变换矩阵的形状 ---------
    X_shape = int(mesh_note[0])
    Y_shape = int(mesh_note[1])
    # --------- 获得k与r值的矩阵 ---------
    k_value = array(wt_data[:, 0]).reshape(Y_shape, X_shape)
    R_value = array(wt_data[:, 1]).reshape(Y_shape, X_shape)
    # --------- 开始绘图 ---------
    plt.close(4)
    fig_WT = plt.figure(4)
    fig_WT.canvas.set_window_title('Plot of mag|W(R,k)|')
    # --------- 判断是否是多列模式，如果是则跳出选择提示 ---------
    if cols > 3:
        if tkinter.messagebox.showinfo(title="Tips",
                                       message="In multiple data mode, only one column of results would be displayed"):
            input_column = tkinter.simpledialog.askinteger("Choose the data you want to show!",
                                                           "Please enter a column number form your data selection " +
                                                           str(col_selection))
            try:
                input_index = col_selection.index(input_column)
            except ValueError:
                tkinter.messagebox.showinfo(title="Error", message="Out of range! Please try again!")
            else:
                W_abs = array(wt_data[:, input_index + 2]).reshape(Y_shape, X_shape)
                plt.contourf(k_value, R_value, W_abs, 30, cmap='rainbow')
                plt.title("Column selection: " + str(input_column))
    else:
        W_abs = array(wt_data[:, 2]).reshape(Y_shape, X_shape)
        plt.contourf(k_value, R_value, W_abs, 30, cmap='rainbow')
    plt.xlabel("k (Å$^{-1}$)")
    plt.ylabel("R (Å)")
    plt.grid()
    plt.xlim(para.Parameters.bmin, para.Parameters.bmax)
    plt.colorbar(shrink=0.8)
    print("Optional: Show the results of wavelet transformation")
    plt.show()


# --------- 逆小波小波结果的展示 ---------
def showInverseWaveletResult():
    # --------- 读入文件 ---------
    kW_data = loadtxt(path.TempPath.get('kW'), skiprows=0)
    reconChi_data = loadtxt(path.TempPath.get('iWT'), skiprows=0)
    col_selection = loadtxt(path.TempPath.get('col_selection'), dtype=int, skiprows=0).tolist()
    # --------- 获得多列数据模式时的列限制 ---------
    cols = kW_data.shape[1]
    # --------- 获得k值（包括原始的和重构的） ---------
    orik = kW_data[:, 0]
    reconk = reconChi_data[:, 0]
    plt.close(5)
    fig_iWT = plt.figure(5)
    fig_iWT.canvas.set_window_title('Plot of inverse wavelet transformation')
    plt.grid()
    plt.xlim(para.Parameters.kmin, para.Parameters.kmax)
    plt.xlabel("k (Å$^{-1}$)")
    plt.ylabel("k-weighted chi (k)")
    if cols > 3:
        if tkinter.messagebox.showinfo(title="Tips",
                                       message="In multiple data mode, only one column of results would be displayed"):
            input_column = tkinter.simpledialog.askinteger("Choose the data you want to show!",
                                                           "Please enter a column number form your data selection " +
                                                           str(col_selection))
            try:
                input_index = col_selection.index(input_column)
            except ValueError:
                tkinter.messagebox.showinfo(title="Error", message="Out of range! Please try again!")
            else:
                temp_orichik = kW_data[:, input_index + 1]
                temp_reconchik = reconChi_data[:, input_index + 1]
                plt.plot(orik, temp_orichik)
                plt.plot(reconk, temp_reconchik)
                plt.title("Column selection: " + str(input_column))
    else:
        temp_orichik = kW_data[:, 1]
        temp_reconchik = reconChi_data[:, 1]
        plt.plot(orik, temp_orichik)
        plt.plot(reconk, temp_reconchik)
    plt.legend(["Original data", "Reconstructed data"], loc='upper right')
    print("Optional: Show reconstructed chi data.")
    plt.show()


def closeFig():
    plt.close(1)
    plt.close(2)
    plt.close(3)
    plt.close(4)
    plt.close(5)
