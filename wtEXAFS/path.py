# -*- coding:utf-8 -*-

from os.path import exists

import os
import sys
import win32con
import win32ui


# ----------- 获取资源路径 -----------
def getResourcePath(relative_path):  # 实现当前路径的定位
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS  # 获取临时资源
    else:
        base_path = os.getcwd()  # 获取当前路径
    return os.path.join(base_path, relative_path)  # 绝对路径


# ----------- 调用winAPI选择获得文件的路径 -----------
def getPath(gettype: str):
    ini_path = getResourcePath(os.path.join("resources", "father_path.txt"))
    if exists(ini_path):
        with open(ini_path, "r", encoding='utf-8') as f:
            ini_dir = f.read()
    else:
        ini_dir = "C:"
    API_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_PATHMUSTEXIST | win32con.OFN_FILEMUSTEXIST
    # --------- 指定获取的文件类型 ---------
    if gettype == "singleData":
        file_type = 'txt File(*.txt)|*.txt|' \
                    'Athena k File(*.chi .chik .chik2 .chik3)|*.chi;*.chik;*.chik2;*.chik3' \
                    '|'
    elif gettype == "multipleData":
        file_type = 'Athena k File(*.chi .chik .chik2 .chik3)|*.chi;*.chik;*.chik2;*.chik3' \
                    '|'
    elif gettype == "config":
        file_type = 'wavelet profile File(*.txt)|*.txt|' \
                    '|'
    else:
        file_type = 'txt File(*.txt)|*.txt|' \
                    '|'
    dlg = win32ui.CreateFileDialog(1, None, None, API_flag, file_type)  # 指定为打开文件窗口
    dlg.SetOFNTitle("Open Data File")
    dlg.SetOFNInitialDir(ini_dir)
    if dlg.DoModal() != win32con.IDOK:
        raise KeyboardInterrupt("User cancelled the process")
    path = dlg.GetPathName()  # 获取文件的路径
    father_path = os.path.dirname(path)
    with open(ini_path, "w", encoding='utf-8') as f:
        f.write(father_path)
    return path


# ----------- 调用winAPI选择保存文件的路径 -----------
def savePath(file_name: str):
    ini_path = getResourcePath(os.path.join("resources", "father_path.txt"))
    if exists(ini_path):
        with open(ini_path, "r", encoding='utf-8') as f:
            ini_dir = f.read()
    else:
        ini_dir = "C:"
    API_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_PATHMUSTEXIST | win32con.OFN_FILEMUSTEXIST
    file_type = 'txt File(*.txt)|*.txt|' \
                '|'
    dlg = win32ui.CreateFileDialog(0, None, file_name, API_flag, file_type)  # 指定为保存文件窗口
    dlg.SetOFNTitle("Save File As")
    dlg.SetOFNInitialDir(ini_dir)  # 默认打开的位置
    if dlg.DoModal() != win32con.IDOK:
        raise KeyboardInterrupt("User cancelled the process")
    path = dlg.GetPathName()  # 获取打开的路径
    return path


def deleteTempFiles():
    for value in TempPath.values():
        if exists(value):
            os.remove(value)
        else:
            pass


# ----------- 临时路径 -----------
TempPath = {
    'k': getResourcePath(os.path.join("resources", "temp_k.txt")),
    'kW': getResourcePath(os.path.join("resources", "temp_kW.txt")),
    'col_selection': getResourcePath(os.path.join("resources", "col_selection.txt")),
    'para_profile': getResourcePath(os.path.join("resources", "temp_paras.txt")),
    'kW_for_WT': getResourcePath(os.path.join("resources", "temp_kWforWT.txt")),
    'window': getResourcePath(os.path.join("resources", "temp_window.txt")),
    'R': getResourcePath(os.path.join("resources", "temp_R.txt")),
    'mother_wavelet': getResourcePath(os.path.join("resources", "temp_MotherWavelet.txt")),
    'energy_coef': getResourcePath(os.path.join("resources", "energy_coef.txt")),
    'wavelet_fft': getResourcePath(os.path.join("resources", "wavelet_fft.txt")),
    'mesh_note': getResourcePath(os.path.join("resources", "mesh.txt")),
    'WT': getResourcePath(os.path.join("resources", "temp_WT.txt")),
    'WT_complex': getResourcePath(os.path.join("resources", "temp_WT_c.txt")),
    'iWT': getResourcePath(os.path.join("resources", "temp_iWT.txt"))
}
