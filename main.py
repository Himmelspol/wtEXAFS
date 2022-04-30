# -*- coding:utf-8 -*-
import os

from wtEXAFS import mainWindow
from wtEXAFS import path

# --------------------- 主程序 ---------------------
if __name__ == "__main__":
    # --------- 实例化主窗体类 ---------
    mainWindow.MainWindow()
    # --------- 删除临时文件 ---------
    path.deleteTempFiles()
    if os.path.exists(path.getResourcePath(os.path.join("resources", "father_path.txt"))):
        os.remove(path.getResourcePath(os.path.join("resources", "father_path.txt")))
    else:
        pass
