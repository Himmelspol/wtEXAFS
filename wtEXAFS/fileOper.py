# -*- coding:utf-8 -*-

from os.path import split

import numpy as np

# ----------- 自定义模块 -----------
from wtEXAFS import para, path, waveletMethod


# --------- txt文件行读入（字符串list模式） ---------
def loadText(path_name: str):
    data_file = open(path_name, 'r', encoding='utf-8')
    data_text = data_file.readlines()
    data_file.close()
    print("Note: Text loaded.")
    return data_text


# ----------- 获得文件的名称（不含扩展名） -----------
def getFileName(path_name: str):
    file_name = split(path_name)[1]
    file_name = file_name.split('.')[0]
    print("Note: File name got.")
    return file_name


# --------- 读入data数据并根据传入参数修改为合适的k数据 ---------
def createPolishedData(path_name: str, row: str, kcol: str, chikcol: list):
    # --------- 初始化参数 ---------
    unpolished_data = np.loadtxt(path_name, skiprows=int(row) - 1, comments="#")
    data_row = len(unpolished_data)
    kcol = int(kcol) - 1
    chikcol = [a - 1 for a in chikcol]
    chikcol.insert(0, kcol)
    # --------- 所需行列转换到新的数组中 ---------
    polished_data = unpolished_data[0:data_row]
    polished_data = polished_data[:, chikcol]
    # --------- 储存为临时的txt文件 ---------
    np.savetxt(path.TempPath.get('k'), polished_data, fmt='%f', delimiter=" ")
    print("Note: k_temp file created.")


# --------- 把k数据处理为kW数据（多列数据处理）并写入txt文件 ---------
def createkWData(kw: int):
    ori_data = np.loadtxt(path.TempPath.get('k'), skiprows=0)
    col_limits = ori_data.shape[1]
    k_data = ori_data[:, 0]
    final_data = k_data
    kW_data = np.ones_like(k_data)
    while kw > 0:
        kW_data = np.multiply(kW_data, k_data)
        kw -= 1
    chikW_data = []
    adp = chikW_data.append
    for i in range(1, col_limits):
        adp(np.multiply(ori_data[:, i], kW_data))
    for i in range(len(chikW_data)):
        final_data = np.column_stack((final_data, chikW_data[i]))
    np.savetxt(path.TempPath.get('kW'), final_data, fmt='%f', delimiter=" ")
    print("Note: kw_temp file created.")


# --------- 保存config临时文件 ---------
def saveConfig():
    temp_para_dict = para.ParaDict()
    with open(path.TempPath.get('para_profile'), 'w') as f:
        f.write("# Please do not change the format of this file!!\n")
        f.write("# This config was extracted from File: " + para.Parameters.file_name + "\n")
        for key, values in temp_para_dict.items():
            f.write(key + " ")
            f.write(str(values) + "\n")
    print("Note: config_temp file created.")


# --------- 返回根据para中设定的k/R序列 ---------
def valueList(type_name: str):
    if type_name == "k+" or type_name == "b+":
        # 为了更高的低r分辨率，将k的取值外拓正负10的区间，k+只用于获得小波基，不更改用户定义的k序列区间
        value_list = np.arange(para.Parameters.bmin - 10.0,
                               para.Parameters.bmax + 10.0 + para.Parameters.db,
                               para.Parameters.db)
    elif type_name == "R" or type_name == "a":
        value_list = np.arange(para.Parameters.Rmin,
                               para.Parameters.Rmax + para.Parameters.dR,
                               para.Parameters.dR)
    else:
        value_list = []
    return value_list


# --------- 构建用户定义kW数据集及其R空间数据（多列数据处理） ---------
def createkWforWT():
    ori_data = np.loadtxt(path.TempPath.get('kW'), skiprows=0)
    col_limits = ori_data.shape[1]
    ori_k = ori_data[:, 0]
    # 根据用户定义的k区间定义窗函数框
    window = waveletMethod.windowFunction(ori_k, para.Parameters.bmin, para.Parameters.bmax, 0.5)
    window_k = np.column_stack((ori_k, window))
    # 构建用于chi数据傅里叶变换的正弦函数基
    polished_k = valueList("k+")
    final_r, sin_base = waveletMethod.sinbase(polished_k)
    # 构成前后增加10Å-1，中间含插值，受到窗函数约束的chi数据
    final_k = polished_k
    new_chikW = []
    new_chiR = []
    for i in range(1, col_limits):
        temp_chi = np.interp(polished_k, ori_k, (ori_data[:, i] * window), left=0.0, right=0.0)  # 首尾补零同时插值
        temp_chiR = waveletMethod.fFT(sin_base, temp_chi, (polished_k[1] - polished_k[0]))  # 傅里叶变换获得R数据
        new_chikW.append(temp_chi)
        new_chiR.append(temp_chiR)
    for i in range(len(new_chikW)):
        final_k = np.column_stack((final_k, new_chikW[i]))
    for i in range(len(new_chiR)):
        final_r = np.column_stack((final_r, new_chiR[i]))
    np.savetxt(path.TempPath.get('kW_for_WT'), final_k, fmt='%f', delimiter=" ")
    np.savetxt(path.TempPath.get('R'), final_r, fmt='%f', delimiter=" ")
    np.savetxt(path.TempPath.get('window'), window_k, fmt='%f', delimiter=" ")
    print("Note: kwForWT_temp file created.")
    print("Note: R_temp file created.")
    print("Note: window_temp file created.")


# --------- 小波基序列的构建（频率r为用户的输入、小波中心b为数据区间的中点） ---------
def mwConstruct(mw_type: str):
    k_input = valueList("k+")
    r_input = valueList("R")
    wavelet_center = (para.Parameters.bmin + para.Parameters.bmax) / 2  # 为了能让小波基的中心与信号中心对齐，设定小波基的中心为信号区间中心
    # 这里构建的小波基为小波的复共轭（为了方便小波变换的运算），同时还获得了能量归一化系数和小波基的FFT结果
    if mw_type == "cauchy":
        wavelet_base = np.array([[waveletMethod.cauchyC(r, wavelet_center, para.Parameters.n, k).conjugate()
                                  for k in k_input] for r in r_input])
        energy_coef = np.array([waveletMethod.energyCoef(r, para.Parameters.n) for r in r_input])
    else:
        # 默认morlet小波
        wavelet_base = np.array(
            [[waveletMethod.morletC(r, wavelet_center, para.Parameters.sigma, para.Parameters.eta, k)
              for k in k_input] for r in r_input])
        energy_coef = np.array([waveletMethod.energyCoef(r, para.Parameters.eta) for r in r_input])
    mw_data = k_input
    for i in range(len(wavelet_base)):
        mw_data = np.column_stack((mw_data, wavelet_base[i]))
    np.savetxt(path.TempPath.get('mother_wavelet'), mw_data, fmt='%f', delimiter=" ")
    np.savetxt(path.TempPath.get('energy_coef'), energy_coef, fmt="%f", delimiter=" ")
    print("Note: waveletBases_temp file created.")
    print("Note: energy_temp file created.")


# --------- 执行小波变换并产生txt临时文件 ---------
def waveleTransformation():
    # --------- 读入需要变换的文件的chi ---------
    for_WT = np.loadtxt(path.TempPath.get('kW_for_WT'), skiprows=0)
    # --------- 读入小波基的原始文件（复数） ---------
    mw_data = np.loadtxt(path.TempPath.get('mother_wavelet'), skiprows=0, dtype=complex)
    # --------- 读入小波基对应的能量 ---------
    energy_coef = np.loadtxt(path.TempPath.get('energy_coef'), skiprows=0)
    # --------- 获取多列文件的列限制 ---------
    col_limits = for_WT.shape[1]
    # --------- 获取k/R序列 ---------
    k_input = valueList("k+")
    R_input = valueList("R")
    # --------- 获取小波基 ---------
    mw_base = mw_data[:, 1:].T
    # --------- 准备获取小波变换结果 ---------
    w_mag = []
    w_complex = []
    for i in range(1, col_limits):
        chi = np.array(for_WT[:, i])
        temp = waveletMethod.cWT(mw_base, chi, energy_coef, para.Parameters.db)
        w_mag.append(temp[0])
        w_complex.append(temp[1])
    # --------- 向结果中加入k与R的数据 ---------
    K, R = np.meshgrid(k_input, R_input)
    mesh_kr = [len(K[0]), len(K)]
    K = np.array(K).flatten()
    R = np.array(R).flatten()
    final_data_mag = np.column_stack((K, R))
    final_data_complex = np.column_stack((K, R))
    for i in range(len(w_mag)):
        final_data_mag = np.column_stack((final_data_mag, w_mag[i]))
        final_data_complex = np.column_stack((final_data_complex, w_complex[i]))
    np.savetxt(path.TempPath.get('mesh_note'), mesh_kr, delimiter=" ")
    np.savetxt(path.TempPath.get('WT'), final_data_mag, fmt='%f', delimiter=" ")
    np.savetxt(path.TempPath.get('WT_complex'), final_data_complex, fmt='%f', delimiter=" ")
    print("Note: mesh_temp file created.")
    print("Note: resultWT_temp file created.")


# --------- 执行小波的逆变换并产生txt临时文件 ---------
def inverseWaveleTransformation():
    # --------- 读入矩阵变形参数 ---------
    mesh_note = np.loadtxt(path.TempPath.get('mesh_note'), skiprows=0)
    X_shape = int(mesh_note[0])
    Y_shape = int(mesh_note[1])
    # --------- 读入小波基对应的能量 ---------
    energy_coef = np.loadtxt(path.TempPath.get('energy_coef'), skiprows=0)
    # --------- 读入小波变换系数并获得系数矩阵（二维，行为r，列为k） ---------
    wt_data = np.loadtxt(path.TempPath.get('WT_complex'), skiprows=0, dtype=complex)
    col_limit = wt_data.shape[1]
    # --------- 构造序列 ---------
    k_input = valueList("k+")
    # --------- 读取获取逆小波变换所需要的小波常数 ---------
    mw_data = np.loadtxt(path.TempPath.get('mother_wavelet'), skiprows=0, dtype=complex)
    wavelet_coef = waveletMethod.fftWavelet(mw_data[:, -1], k_input)  # 读取其中一个小波进行傅里叶变换即可
    # ------- 准备获取小波逆变换的结果 -----------
    chi_recon = []
    for i in range(2, col_limit):
        w_matrix = np.array(wt_data[:, i]).reshape(Y_shape, X_shape)
        temp = waveletMethod.iWT(w_matrix, energy_coef, wavelet_coef)
        chi_recon.append(temp)
    # --------- 向结果中加入k的数据（同时裁剪重构后的数据） ---------
    data_index = np.where(
        np.logical_and(k_input >= para.Parameters.kmin, k_input <= para.Parameters.kmax))  # 获取与原数据区间对应的索引
    final_data = k_input[data_index]
    for i in range(len(chi_recon)):
        final_data = np.column_stack((final_data, chi_recon[i][data_index]))
    np.savetxt(path.TempPath.get('iWT'), final_data, fmt='%f', delimiter=" ")
